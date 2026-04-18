from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import Http404

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import JobDescriptionSerializer, JobDescription, ResumeSerializer, Resume
from .analyzer import process_resume
from .models import AnalysisResult


# Template Views
class IndexView(TemplateView):
    template_name = 'index.html'


class AnalyzeView(TemplateView):
    template_name = 'analyze.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jobs'] = JobDescription.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        try:
            resume_file = request.FILES.get('resume')
            job_description_id = request.POST.get('job_description')

            if not resume_file:
                messages.error(request, 'Please upload a resume file.')
                return redirect('analyze')

            if not job_description_id:
                messages.error(request, 'Please select a job description.')
                return redirect('analyze')

            # Validate file type
            if not resume_file.name.lower().endswith('.pdf'):
                messages.error(request, 'Please upload a PDF file only.')
                return redirect('analyze')

            # Validate file size (10MB limit)
            if resume_file.size > 10 * 1024 * 1024:
                messages.error(request, 'File size must be less than 10MB.')
                return redirect('analyze')

            # Save resume to instance
            resume = Resume(resume=resume_file, filename=resume_file.name)
            resume.save()

            # Get job description
            try:
                job = JobDescription.objects.get(id=job_description_id)
            except JobDescription.DoesNotExist:
                messages.error(request, 'Selected job description not found.')
                return redirect('analyze')

            # Get resume path
            resume_path = resume.resume.path

            # Process resume
            try:
                results = process_resume(resume_path, job.job_description)

                if not results:
                    messages.error(request, 'Failed to analyze the resume. Please try again.')
                    return redirect('analyze')

                # Save analysis result
                analysis = AnalysisResult.objects.create(
                    resume=resume,
                    job_description=job,
                    rank=results.get('rank', 0),
                    skills=results.get('skills', []),
                    total_experience=results.get('total_experience', 'Unknown'),
                    project_categories=results.get('project_category', []),
                    resume_summary=results.get('resume_summary', ''),
                    raw_data=results
                )

                # Store analysis ID in session for results page
                request.session['last_analysis_id'] = analysis.id

                # Show summary on analyze page and redirect to results
                messages.success(request, f'Analysis complete! Match score: {analysis.rank}%')
                return render(request, 'results.html', {
                    'results': results,
                    'analysis': analysis
                })

            except Exception as e:
                messages.error(request, f'Analysis failed: {str(e)}')
                return redirect('analyze')

        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}')
            return redirect('analyze')


class JobDescriptionsView(ListView):
    model = JobDescription
    template_name = 'job_descriptions.html'
    context_object_name = 'jobs'
    paginate_by = 10


class JobDetailView(DetailView):
    model = JobDescription
    template_name = 'job_detail.html'
    context_object_name = 'job'


class JobFormView(CreateView):
    model = JobDescription
    template_name = 'job_form.html'
    fields = ['job_title', 'job_description']
    success_url = reverse_lazy('job-descriptions')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = None
        return context


class JobEditView(UpdateView):
    model = JobDescription
    template_name = 'job_form.html'
    fields = ['job_title', 'job_description']
    success_url = reverse_lazy('job-descriptions')
    context_object_name = 'job'


class JobDeleteView(DeleteView):
    model = JobDescription
    template_name = 'job_confirm_delete.html'
    success_url = reverse_lazy('job-descriptions')


class AnalysisHistoryView(ListView):
    model = AnalysisResult
    template_name = 'analysis_history.html'
    context_object_name = 'analyses'
    paginate_by = 10

    def get_queryset(self):
        return AnalysisResult.objects.select_related('resume', 'job_description').order_by('-analyzed_at')


class AnalysisDetailView(DetailView):
    model = AnalysisResult
    template_name = 'analysis_detail.html'
    context_object_name = 'analysis'

    def get_object(self):
        analysis = super().get_object()
        # Convert raw_data back to results format for template compatibility
        analysis.results = analysis.raw_data
        return analysis


class CompareAnalysesView(TemplateView):
    template_name = 'compare_analyses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        analysis_ids_raw = self.request.GET.getlist('ids')
        
        analysis_ids = []
        for raw_id in analysis_ids_raw:
            if ',' in raw_id:
                analysis_ids.extend([i.strip() for i in raw_id.split(',') if i.strip()])
            else:
                if raw_id.strip():
                    analysis_ids.append(raw_id.strip())

        if analysis_ids:
            analyses = AnalysisResult.objects.filter(id__in=analysis_ids).select_related('resume', 'job_description')
            context['analyses'] = analyses
            context['comparison_data'] = self.prepare_comparison_data(analyses)

        context['all_analyses'] = AnalysisResult.objects.select_related('resume', 'job_description').order_by('-analyzed_at')[:20]
        return context

    def prepare_comparison_data(self, analyses):
        """Prepare data for side-by-side comparison"""
        comparison = []
        for analysis in analyses:
            comparison.append({
                'id': analysis.id,
                'resume_name': analysis.resume.filename,
                'job_title': analysis.job_description.job_title,
                'rank': analysis.rank,
                'total_experience': analysis.total_experience,
                'skills_count': len(analysis.skills),
                'skills': analysis.skills,
                'project_categories': analysis.project_categories,
                'resume_summary': analysis.resume_summary,
                'analyzed_at': analysis.analyzed_at,
            })
        return comparison


# API Views
class JobDescriptionAPI(APIView):
    def get(self , request):
        queryset = JobDescription.objects.all()
        serializer = JobDescriptionSerializer(queryset, many = True)
        return Response({
            'status' : True,
            'data' : serializer.data
        })
    

class AnalyzeResumeAPI(APIView):
    def post(self , request):
        try:
            data = request.data
            if not data.get('job_description'):
                return Response({
                    'status' : False,
                    'message' : 'job_description is required',
                    'data' : {}
                })
            
            serializer = ResumeSerializer(data = data)
            if not serializer.is_valid():
                return Response({
                        'status' : False,
                        'message' : 'errors',
                        'data' : serializer.errors
                    })
            
            serializer.save()
            _data = serializer.data
            resume_instance = Resume.objects.get(id = _data['id'])
            resume_path = resume_instance.resume.path
            data = process_resume(resume_path, 
                                  JobDescription.objects.get(id =data.get('job_description') ).job_description
                                  )           
            return Response({
                        'status' : True,
                        'message' : 'resume analyzed',
                        'data' : data
                    })
        except Exception as e:
            return Response({
                'status' : False,
                'message' : 'An error occurred while analyzing the resume',
                'data' : {}
            })
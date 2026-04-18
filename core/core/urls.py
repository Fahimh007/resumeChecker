"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from resumeChecker.views import (
    IndexView, AnalyzeView, JobDescriptionsView, JobDetailView, 
    JobFormView, JobEditView, JobDeleteView,
    AnalysisHistoryView, AnalysisDetailView, CompareAnalysesView,
    JobDescriptionAPI, AnalyzeResumeAPI
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Template Views
    path('', IndexView.as_view(), name='index'),
    path('analyze/', AnalyzeView.as_view(), name='analyze'),
    path('job-descriptions/', JobDescriptionsView.as_view(), name='job-descriptions'),
    path('job-descriptions/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('job-descriptions/add/', JobFormView.as_view(), name='job-form'),
    path('job-descriptions/<int:pk>/edit/', JobEditView.as_view(), name='job-edit'),
    path('job-descriptions/<int:pk>/delete/', JobDeleteView.as_view(), name='job-delete'),
    
    # Analysis Views
    path('analyses/', AnalysisHistoryView.as_view(), name='analysis-history'),
    path('analyses/<int:pk>/', AnalysisDetailView.as_view(), name='analysis-detail'),
    path('compare/', CompareAnalysesView.as_view(), name='compare-analyses'),
    
    # API Views
    path('api/jobs/', JobDescriptionAPI.as_view()),
    path('api/resume/', AnalyzeResumeAPI.as_view()),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
 
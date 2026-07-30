from abc import ABC, abstractmethod

from app.resume_exports.renderers.models import RenderedResume
from app.resumes.models import Resume


class ResumeExportRenderer(ABC):
    """
    Abstract interface for resume export renderers.

    Concrete renderers are responsible for converting a fully loaded
    Resume entity into a downloadable document.
    """

    @property
    @abstractmethod
    def media_type(self) -> str:
        """
        Return the MIME type produced by the renderer.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def file_extension(self) -> str:
        """
        Return the generated file extension without a leading dot.
        """
        raise NotImplementedError

    @abstractmethod
    def render(
        self,
        resume: Resume,
    ) -> RenderedResume:
        """
        Render a fully loaded resume into a downloadable document.
        """
        raise NotImplementedError
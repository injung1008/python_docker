from dataclasses import dataclass

#데이터를 은닉화 한다음 필요할 때 꺼내쓰는 개념
@dataclass
class FileDTO(object):

    context: str
    fname: str
    url = str
    dframe: object


    @property
    def context(self) -> str: return self._context

    @context.setter
    def context(self, context):
        self._context = context

    @property
    def fname(self) -> str: return self._fname

    @fname.setter
    def fname(self, fname): self._fname = fname

    @property
    def dframe(self) -> object: return self._dframe

    @dframe.setter
    def dframe(self, dframe): self._dframe = dframe

    @property
    def url(self) -> object: return self._url

    @dframe.setter
    def url(self, dframe): self._url = url
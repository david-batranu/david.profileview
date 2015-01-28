import cProfile
import marshal
import json
from StringIO import StringIO
from Products.Five.browser import BrowserView


class ProfileView(BrowserView):

    def prepare_download(self, profile):
        profile.create_stats()
        dump = marshal.dumps(profile.stats)

        stream = StringIO()
        stream.write(dump)

        stream.seek(0)

        return stream

    def set_headers(self, name=''):
        self.request.response.setHeader(
            'Content-Type', 'application/octet-steam')
        filename = name or self.context.__name__
        content_disp = 'attachment; filename={0}.profile'.format(filename)
        self.request.response.setHeader(
            'Content-Disposition', content_disp)

    def download(self, profile, name=''):
        stream = self.prepare_download(profile)
        self.set_headers(name)
        return stream.read()

    def default(self, **kwargs):
        profiler = cProfile.Profile()
        profiler.runcall(self.context, **kwargs)
        return profiler

    def targeted(self, target, **kwargs):
        profiler = cProfile.Profile()
        profiler.runcall(getattr(self.context, target), **kwargs)
        return profiler

    def main(self, target=None, **kwargs):
        if 'target' in self.request:
            target = self.request.get('target')

        if 'kwargs' in self.request:
            kwargs = json.loads(self.request.get('kwargs', '{}'))

        if target is not None:
            profile = self.targeted(target, **kwargs)
        else:
            profile = self.default(**kwargs)

        return self.download(profile, name=target)


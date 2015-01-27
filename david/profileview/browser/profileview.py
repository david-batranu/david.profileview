import cProfile
import marshal
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
        self.request.response.setHeader('Content-Type', 'application/octet-steam')
        filename = name or self.context.__name__
        content_disposition = 'attachment; filename={0}.profile'.format(filename)
        self.request.response.setHeader('Content-Disposition', content_disposition)

    def download(self, profile, name=''):
        stream = self.prepare_download(profile)
        self.set_headers(name)
        return stream.read()

    def default(self):
        profiler = cProfile.Profile()
        profiler.runcall(self.context)
        return profiler

    def targeted(self, target):
        profiler = cProfile.Profile()
        profiler.runcall(getattr(self.context, target))
        return profiler

    def main(self, target=None):
        if 'target' in self.request:
            target = self.request.get('target')

        if target is not None:
            profile = self.targeted(target)
        else:
            profile = self.default()

        return self.download(profile, name=target)


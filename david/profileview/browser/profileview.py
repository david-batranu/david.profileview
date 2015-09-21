import os
import pstats
import cProfile
import marshal
import json
import tempfile
from StringIO import StringIO
from Products.Five.browser import BrowserView

from plone import api


def jsonify(request, data, cache=False):
    header = request.RESPONSE.setHeader
    header("Content-Type", "application/json")
    if cache:
        header("Expires", "Sun, 17-Jan-2038 19:14:07 GMT")
    return json.dumps(data, indent=2, sort_keys=True)


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

        try:
            profiler.runcall(getattr(self.context, target), **kwargs)
        except AttributeError:
            view = self.context.restrictedTraverse(target)
            profiler.runcall(view, **kwargs)

        return profiler

    def run_profile(self, target=None, **kwargs):
        if 'target' in self.request:
            target = self.request.get('target')

        if 'kwargs' in self.request:
            kwargs = json.loads(self.request.get('kwargs', '{}'))

        if target is not None:
            return (self.targeted(target, **kwargs), target)
        else:
            return (self.default(**kwargs), self.context.__name__)

    def main(self):
        profile, target = self.run_profile()
        return self.download(profile, name=target)

    def make_temp(self):
        profile, name = self.run_profile()
        handle, path = tempfile.mkstemp('.profile', name + '_')
        profile.dump_stats(path)
        os.close(handle)
        return path

    def query_stats(self, stats, line):
        command = [x.strip() for x in line.strip().split(' ')]
        cmd, qargs = command[0], command[1:]
        qargs = [int(arg) if arg.isdigit() else arg for arg in qargs]

        if cmd == 'sort':
            stats.sort_stats(*qargs)
        elif cmd == 'reverse':
            stats.reverse_order()
        elif cmd == 'strip':
            stats.strip_dirs()
        elif cmd in ['callers', 'callees', 'stats']:
            return cmd, qargs

    def ajax(self):
        path = self.request.get('path', '')
        query = json.loads(self.request.get('query', '[]'))

        if not path:
            path = self.make_temp()

        stats_out = StringIO()
        stats = pstats.Stats(path, stream=stats_out)

        query_result = None
        for line in query:
            query_result = self.query_stats(stats, line)
            if query_result:
                break

        if query_result is None:
            query_result = ('stats', '')

        qcmd, qargs = query_result
        if qcmd == 'callers':
            stats.print_callers(*qargs)
        elif qcmd == 'callees':
            stats.print_callees(*qargs)
        elif qcmd == 'stats':
            stats.print_stats(*qargs)

        stats_out.seek(0)

        result = {
            'profile': path,
            'data': stats_out.read()
        }

        return jsonify(self.request, result)

    @property
    def site_url(self):
        return api.portal.get().absolute_url()

    @property
    def context_name(self):
        try:
            return self.request.get('target',  self.context.__name__)
        except:
            return 'Unknown context'

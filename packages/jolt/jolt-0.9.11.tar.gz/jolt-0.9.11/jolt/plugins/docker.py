from jolt import config
from jolt import scheduler
from jolt import Tools
from jolt.manifest import JoltManifest
from io import StringIO


class ContainerExecutor(scheduler.Executor):
    def __init__(self, factory, task, force_upload=False, force_build=False):
        super(ContainerExecutor, self).__init__(factory)
        self.factory = factory
        self.task = task

    def _create_manifest(self):
        manifest = JoltManifest.export(self.task)
        build = manifest.create_build()

        tasks = [self.task.qualified_name]
        tasks += [t.qualified_name for t in self.task.extensions]

        for task in tasks:
            mt = build.create_task()
            mt.name = task

        for task in self.factory.options.default:
            default = build.create_default()
            default.name = task

        registry = scheduler.ExecutorRegistry.get()
        for key, value in registry.get_network_parameters(self.task).items():
            param = manifest.create_parameter()
            param.key = key
            param.value = value

        strio = StringIO()
        config._file.write(strio)
        manifest.config = strio.getvalue()

        return manifest.format()

    def run(self, env):
        if self.is_aborted():
            return

        t = Tools(self.task.task)
        with t.tmpdir("docker") as tmp: #, t.cwd(tmp.path):
            manifest = self._create_manifest()
            t.write_file("default.joltxmanifest", manifest)
            self.task.started()
            self.task.running()
            t.run("docker run -w {joltdir} -v {joltdir}:{joltdir} jolt:latest jolt build --worker", tmp.path)
            self.task.finished()

        return self.task


scheduler.LocalExecutor = ContainerExecutor

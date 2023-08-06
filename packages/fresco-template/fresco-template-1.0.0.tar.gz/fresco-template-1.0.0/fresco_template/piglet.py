# Copyright 2016 Oliver Cope
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .core import BasePlugin, TemplateEnvironment


class PigletPlugin(BasePlugin):
    def __init__(self, loader):
        self.loader = loader.load

    def render(self, template_name, context, stream):
        tmpl = self.loader(template_name)
        if stream:
            return tmpl(context)
        return tmpl.render(context)


class Piglet(TemplateEnvironment):
    plugin_class = PigletPlugin

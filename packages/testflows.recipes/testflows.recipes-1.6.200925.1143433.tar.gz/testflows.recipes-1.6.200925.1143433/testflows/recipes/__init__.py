# Copyright 2020 Katteli Inc.
# TestFlows.com Open-Source Software Testing Framework (http://testflows.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
__author__ = "Vitaliy Zakaznikov"
__version__ = "1.6.200925.1143433"
__license__ = f"""
Copyright 2020 Katteli Inc.
TestFlows.com Open-Source Software Testing Framework (http://testflows.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License
"""
import os
import sys

from testflows.connect import Shell
from testflows.asserts import error, errors

from .core import *

__all__ = [
        "os", "sys",
        "Shell", "error", "errors",
        "RecipeModule", "RecipeSuite", "RecipePlan", "RecipeStep",
        "Step", "Given", "When", "Then", "But", "By", "Finally",
        "Name", "Description", "Uid", "Tags", "Args",
        "Flags",
        "OK", "XOK", "Fail", "XFail", "Skip", "Error", "XError", "Null", "XNull",
        "XFails", "XFlags", "Repeat",
        "Attributes", "ArgumentParser",
        "Tag", "Argument", "Attribute", "Requirement", "Metric", "Ticket", "Value",
        "Table",
        "The", "TheTags",
        "top", "current", "previous", "load", "append_path",
        "main", "args",
        "metric", "ticket", "value", "note", "debug", "trace",
        "message", "exception", "ok", "fail", "skip", "err",
        "null", "xok", "xfail", "xerr", "xnull", "pause", "getsattr",
        "current_dir", "current_module", "load_module",
        "TE", "UT", "SKIP", "EOK", "EFAIL", "EERROR", "ESKIP",
        "XOK", "XFAIL", "XERROR", "XNULL",
        "FAIL_NOT_COUNTED", "ERROR_NOT_COUNTED", "NULL_NOT_COUNTED",
        "PAUSE", "PAUSE_BEFORE", "PAUSE_AFTER", "REPORT", "DOCUMENT",
        "MANDATORY", "CLEAR",
        "EANY", "ERESULT", "XRESULT",
        "__author__", "__version__", "__license__",
        "threading"
    ]

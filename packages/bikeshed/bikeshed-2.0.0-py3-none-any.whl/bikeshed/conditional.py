# -*- coding: utf-8 -*-

import re

from . import config
from .h import *
from .messages import *

# Any element can have an include-if or exclude-if attribute,
# containing a comma-separated list of conditions (described below).
# If an element has include-if, it must match at least one condition,
# or else it's removed from the document.
# If an element has exclude-if, if it matches at least one condition,
# it's removed from the document.
# (An element can have both; both of the above conditions apply.)
#
# A condition is either a Status value, or a `!Foo: bar` custom metadata declaration,
# which is compared literally after trimming.
#
# The <if-wrapper> element is a special wrapper element
# that exists *solely* to support conditional inclusion,
# and which never appears in the output document.
# It must have a conditional attribute on it,
# and if it passes the checks,
# it's still removed from the document,
# but its children are left in its place.


def processConditionals(doc):
	for el in findAll("[include-if], [exclude-if], if-wrapper", doc):
		if el.tag == "if-wrapper" and not hasAttr(el, "include-if", "exclude-if"):
			die("<if-wrapper> elements must have an include-if and/or exclude-if attribute.", el=el)
			removeNode(el)
			continue

		removeEl = False
		if hasAttr(el, "include-if"):
			if not any(evalConditions(doc, el, el.get("include-if"))):
				removeEl = True
		if not removeEl and hasAttr(el, "exclude-if"):
			if any(evalConditions(doc, el, el.get("exclude-if"))):
				removeEl = True

		if removeEl:
			removeNode(el)
			continue

		if el.tag == "if-wrapper":
			# Passed the tests, so just remove the wrapper
			replaceNode(el, *childNodes(el, clear=True))
			continue

		# Otherwise, go ahead and just remove the include/exclude-if attributes,
		# since they're non-standard
		removeAttr(el, "include-if", "exclude-if")


def evalConditions(doc, el, conditionString):
	for cond in parseConditions(conditionString, el):
		if cond['type'] == "status":
			if not config.looselyMatch(cond['value'], doc.md.status):
				yield False
			else:
				yield True
		else:
			die(f"Program error, some type of include/exclude-if condition wasn't handled: '{repr(cond)}'. Please report!", el)
			yield False


def parseConditions(s, el=None):
	for sub in s.split(","):
		sub = sub.strip()
		if sub == "":
			continue
		if re.match(r"([\w-]+/)?[\w-]+$", sub):
			yield {"type":"status", "value": sub}
			continue
		die(f"Unknown include/exclude-if condition '{sub}'", el=el)
		continue
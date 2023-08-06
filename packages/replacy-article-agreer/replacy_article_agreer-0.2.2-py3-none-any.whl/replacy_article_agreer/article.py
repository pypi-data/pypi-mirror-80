from typing import List

import inflect
from spacy.tokens import Span


inflector = inflect.engine()


class ReplacyPipelineOrderError(RuntimeError):
    pass


class ArticleAgreer:
    def __init__(self, name="ArticleAgreer"):
        self.name = name

    @staticmethod
    def _remove_article_prefix_with_whitespace(text: str):
        if not isinstance(text, str):
            raise ReplacyPipelineOrderError(
                "ArticleAgreer replaCy component must be added after joiner component\
                in order to operate on text suggestions"
            )
        if text.startswith("a "):
            return text[2:]
        elif text.startswith("an "):
            return text[3:]
        else:
            return text

    @staticmethod
    def fix_double_article(s: Span) -> Span:
        potential_problem = (
            s.doc[s.start - 1].lower_ in ["a", "an"] if s.start > 0 else False
        )
        if potential_problem:
            new_suggestions = [
                ArticleAgreer._remove_article_prefix_with_whitespace(suggestion)
                for suggestion in s._.suggestions
            ]
            s._.suggestions = new_suggestions
        return s

    @staticmethod
    def fix_a_an(s: Span) -> Span:
        """
        Always call after fix_double_article, so we can assume
        that suggestion starts with a/an xor suggestion is preceded by a/an
        """
        a_an_before_suggestion = (
            s.doc[s.start - 1].lower_ in ["a", "an"] if s.start > 0 else False
        )
        suggestions_starting_with_a_an = []
        for i, suggestion in enumerate(s._.suggestions):
            if suggestion.startswith("a ") or suggestion.startswith("an "):
                suggestions_starting_with_a_an.append(i)

        if a_an_before_suggestion:
            update_span = True
            # need to make the new span extend 1 back to catch the a/an
            # then modify each suggestion
            new_span = s.doc[s.start - 1 : s.end]
            for k in s._.span_extensions.keys():
                setattr(new_span._, k, getattr(s._, k))
            new_span._.suggestions = [
                inflector.a(suggestion) for suggestion in s._.suggestions
            ]
            if len(new_span._.suggestions):
                orig_and_corr_start_with_a = (
                    new_span.text[:2] == "a " and new_span._.suggestions[0][:2] == "a "
                )
                orig_and_corr_start_with_an = (
                    new_span.text[:3] == "an "
                    and new_span._.suggestions[0][:3] == "an "
                )
                same_article = orig_and_corr_start_with_a or orig_and_corr_start_with_an
                if same_article:
                    update_span = False
            s = new_span if update_span else s
        elif len(suggestions_starting_with_a_an):
            new_suggestions = [
                inflector.a(suggestion) for suggestion in s._.suggestions
            ]
            s._.suggestions = new_suggestions
        return s

    @staticmethod
    def fix(s: Span) -> Span:
        s = ArticleAgreer.fix_double_article(s)
        s = ArticleAgreer.fix_a_an(s)
        return s

    def __call__(self, spans: List[Span]) -> List[Span]:
        return [self.fix(s) for s in spans]
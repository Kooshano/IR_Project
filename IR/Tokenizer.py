import re
from pathlib import Path
from typing import List
from nltk.tokenize.api import TokenizerI


class Tokenizer(TokenizerI):
    def __init__(
        self: "Tokenizer",
        join_verb_parts: bool = True,
        replace_links: bool = True,
        replace_ids: bool = True,
        replace_emails: bool = True,
        replace_hashtags: bool = True,
    ) -> None:
        self.verbs_file_open = Path("verbs.dat").open(encoding="utf8")
        self.verbs = self.verbs_file_open.readlines()
        self.bons = {verb.split("#")[0] for verb in self.verbs}
        self.verbe = set(
            [bon + "ه" for bon in self.bons]
            +
            ["ن" + bon + "ه" for bon in self.bons],
            )
        self._join_verb_parts = join_verb_parts
        self.replace_links = replace_links
        self.replace_ids = replace_ids
        self.replace_emails = replace_emails
        self.replace_hashtags = replace_hashtags
        self.pattern = re.compile(r'([؟!?]+|[\d.:]+|[:.،؛»\])}"«\[({/\\])')  # TODO \d
        self.id_pattern = re.compile(r"(?<![\w._])(@[\w_]+)")
        self.id_repl = r" ID "
        self.link_pattern = re.compile(
            r"((https?|ftp)://)?(?<!@)(([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})[-\w@:%_.+/~#?=&]*",
        )
        self.link_repl = r" LINK "
        self.email_pattern = re.compile(
            r"[a-zA-Z0-9._+-]+@([a-zA-Z0-9-]+\.)+[A-Za-z]{2,}",
        )
        self.email_repl = r" EMAIL "



        if join_verb_parts:
            self.after_verbs = {
                "ام",
                "ای",
                "است",
                "ایم",
                "اید",
                "اند",
                "بودم",
                "بودی",
                "بود",
                "بودیم",
                "بودید",
                "بودند",
                "باشم",
                "باشی",
                "باشد",
                "باشیم",
                "باشید",
                "باشند",
                "شده_ام",
                "شده_ای",
                "شده_است",
                "شده_ایم",
                "شده_اید",
                "شده_اند",
                "شده_بودم",
                "شده_بودی",
                "شده_بود",
                "شده_بودیم",
                "شده_بودید",
                "شده_بودند",
                "شده_باشم",
                "شده_باشی",
                "شده_باشد",
                "شده_باشیم",
                "شده_باشید",
                "شده_باشند",
                "نشده_ام",
                "نشده_ای",
                "نشده_است",
                "نشده_ایم",
                "نشده_اید",
                "نشده_اند",
                "نشده_بودم",
                "نشده_بودی",
                "نشده_بود",
                "نشده_بودیم",
                "نشده_بودید",
                "نشده_بودند",
                "نشده_باشم",
                "نشده_باشی",
                "نشده_باشد",
                "نشده_باشیم",
                "نشده_باشید",
                "نشده_باشند",
                "شوم",
                "شوی",
                "شود",
                "شویم",
                "شوید",
                "شوند",
                "شدم",
                "شدی",
                "شد",
                "شدیم",
                "شدید",
                "شدند",
                "نشوم",
                "نشوی",
                "نشود",
                "نشویم",
                "نشوید",
                "نشوند",
                "نشدم",
                "نشدی",
                "نشد",
                "نشدیم",
                "نشدید",
                "نشدند",
                "می‌شوم",
                "می‌شوی",
                "می‌شود",
                "می‌شویم",
                "می‌شوید",
                "می‌شوند",
                "می‌شدم",
                "می‌شدی",
                "می‌شد",
                "می‌شدیم",
                "می‌شدید",
                "می‌شدند",
                "نمی‌شوم",
                "نمی‌شوی",
                "نمی‌شود",
                "نمی‌شویم",
                "نمی‌شوید",
                "نمی‌شوند",
                "نمی‌شدم",
                "نمی‌شدی",
                "نمی‌شد",
                "نمی‌شدیم",
                "نمی‌شدید",
                "نمی‌شدند",
                "خواهم_شد",
                "خواهی_شد",
                "خواهد_شد",
                "خواهیم_شد",
                "خواهید_شد",
                "خواهند_شد",
                "نخواهم_شد",
                "نخواهی_شد",
                "نخواهد_شد",
                "نخواهیم_شد",
                "نخواهید_شد",
                "نخواهند_شد",
            }

            self.before_verbs = {
                "خواهم",
                "خواهی",
                "خواهد",
                "خواهیم",
                "خواهید",
                "خواهند",
                "نخواهم",
                "نخواهی",
                "نخواهد",
                "نخواهیم",
                "نخواهید",
                "نخواهند",
            }

    def tokenize(self: "Tokenizer", text: str) -> List[str]:

        if self.replace_emails:
            text = self.email_pattern.sub(self.email_repl, text)
        if self.replace_links:
            text = self.link_pattern.sub(self.link_repl, text)
        if self.replace_ids:
            text = self.id_pattern.sub(self.id_repl, text)
        text = self.pattern.sub(r" \1 ", text.replace("\n", " ").replace("\t", " "))

        tokens = [word for word in text.split(" ") if word]

        tokens = self.join_verb_parts(tokens) if self._join_verb_parts else tokens

        return tokens




    def join_verb_parts(self: "Tokenizer", tokens: List[str]) -> List[str]:
        if len(tokens) == 1:
            return tokens

        result = [""]
        for token in reversed(tokens):
            if token in self.before_verbs or (
                result[-1] in self.after_verbs and token in self.verbe
            ):
                result[-1] = token + "_" + result[-1]
            else:
                result.append(token)
        return list(reversed(result[1:]))

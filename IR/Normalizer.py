import re
from typing import List
from Tokenizer import Tokenizer
from pathlib import Path

def maketrans(a: str, b: str):

    return {ord(a): b for a, b in zip(a, b)}
def regex_replace(patterns: str, text: str) -> str:
    for pattern, repl in patterns:
        text = re.sub(pattern, repl, text)
    return text
class Normalizer:

    def __init__(
        self: "Normalizer",
        correct_spacing: bool = True,
        remove_diacritics: bool = True,
        persian_style: bool = True,
        persian_numbers: bool = True,
        unicodes_replacement: bool = True,
        seperate_mi: bool = True,
    ) -> None:
        self._correct_spacing = correct_spacing
        self._remove_diacritics = remove_diacritics
        self._persian_style = persian_style
        self._persian_number = persian_numbers
        self._unicodes_replacement = unicodes_replacement
        self._seperate_mi = seperate_mi

        self.translation_src = "ؠػػؽؾؿكيٮٯٷٸٹٺٻټٽٿڀځٵٶٷٸٹٺٻټٽٿڀځڂڅڇڈډڊڋڌڍڎڏڐڑڒړڔڕږڗڙښڛڜڝڞڟڠڡڢڣڤڥڦڧڨڪګڬڭڮڰڱڲڳڴڵڶڷڸڹںڻڼڽھڿہۂۃۄۅۆۇۈۉۊۋۏۍێېۑےۓەۮۯۺۻۼۿݐݑݒݓݔݕݖݗݘݙݚݛݜݝݞݟݠݡݢݣݤݥݦݧݨݩݪݫݬݭݮݯݰݱݲݳݴݵݶݷݸݹݺݻݼݽݾݿࢠࢡࢢࢣࢤࢥࢦࢧࢨࢩࢪࢫࢮࢯࢰࢱࢬࢲࢳࢴࢶࢷࢸࢹࢺࢻࢼࢽﭐﭑﭒﭓﭔﭕﭖﭗﭘﭙﭚﭛﭜﭝﭞﭟﭠﭡﭢﭣﭤﭥﭦﭧﭨﭩﭮﭯﭰﭱﭲﭳﭴﭵﭶﭷﭸﭹﭺﭻﭼﭽﭾﭿﮀﮁﮂﮃﮄﮅﮆﮇﮈﮉﮊﮋﮌﮍﮎﮏﮐﮑﮒﮓﮔﮕﮖﮗﮘﮙﮚﮛﮜﮝﮞﮟﮠﮡﮢﮣﮤﮥﮦﮧﮨﮩﮪﮫﮬﮭﮮﮯﮰﮱﺀﺁﺃﺄﺅﺆﺇﺈﺉﺊﺋﺌﺍﺎﺏﺐﺑﺒﺕﺖﺗﺘﺙﺚﺛﺜﺝﺞﺟﺠﺡﺢﺣﺤﺥﺦﺧﺨﺩﺪﺫﺬﺭﺮﺯﺰﺱﺲﺳﺴﺵﺶﺷﺸﺹﺺﺻﺼﺽﺾﺿﻀﻁﻂﻃﻄﻅﻆﻇﻈﻉﻊﻋﻌﻍﻎﻏﻐﻑﻒﻓﻔﻕﻖﻗﻘﻙﻚﻛﻜﻝﻞﻟﻠﻡﻢﻣﻤﻥﻦﻧﻨﻩﻪﻫﻬﻭﻮﻯﻰﻱﻲﻳﻴىكي“” "
        self.translation_dst = (
            'یککیییکیبقویتتبتتتبحاوویتتبتتتبحححچدددددددددررررررررسسسصصطعففففففققکککککگگگگگللللنننننهچهههوووووووووییییییهدرشضغهبببببببححددرسعععففکککممنننلررسححسرحاایییووییحسسکببجطفقلمییرودصگویزعکبپتریفقنااببببپپپپببببتتتتتتتتتتتتففففححححححححچچچچچچچچددددددددژژررککککگگگگگگگگگگگگننننننههههههههههییییءاااووااییییااببببتتتتثثثثججججححححخخخخددذذررززسسسسششششصصصصضضضضططططظظظظععععغغغغففففققققککککللللممممننننههههوویییییییکی"" '
        )
        self.verbs_file_open = Path("verbs.dat").open(encoding="utf8")
        self.verbs = self.verbs_file_open.readlines()
        self.bons = {verb.split("#")[0] for verb in self.verbs}
        self.verbe = set(
            [bon + "ه" for bon in self.bons]
            +
            ["ن" + bon + "ه" for bon in self.bons],
            )
        self.words_file_open = Path("words.dat").open(encoding="utf8")
        self.words = self.words_file_open.readlines()
        self.words = {word.split("#")[0]: word.split("#")[1:] for word in self.words}
        
        if self._correct_spacing or self._decrease_repeated_chars:
            self.tokenizer = Tokenizer(join_verb_parts=False)

        if self._persian_number:
            self.number_translation_src = "0123456789%٠١٢٣٤٥٦٧٨٩"
            self.number_translation_dst = "۰۱۲۳۴۵۶۷۸۹٪۰۱۲۳۴۵۶۷۸۹"

        if self._correct_spacing:
            self.suffixes = {
                "ی",
                "ای",
                "ها",
                "های",
                "هایی",
                "تر",
                "تری",
                "ترین",
                "گر",
                "گری",
                "ام",
                "ات",
                "اش",
            }

            self.extra_space_patterns = [
                (r" {2,}", " "),  # remove extra spaces
                (r"\n{3,}", "\n\n"),  # remove extra newlines
                (r"\u200c{2,}", "\u200c"),  # remove extra ZWNJs
                (r"\u200c{1,} ", " "),  # remove unneded ZWNJs before space
                (r" \u200c{1,}", " "),  # remove unneded ZWNJs after space
                (r"\b\u200c*\B", ""),  # remove unneded ZWNJs at the beginning of words
                (r"\B\u200c*\b", ""),  # remove unneded ZWNJs at the end of words
                (r"[ـ\r]", ""),  # remove keshide, carriage returns
            ]

            punc_after, punc_before = r"\.:!،؛؟»\]\)\}", r"«\[\(\{"

            self.punctuation_spacing_patterns = [
                # remove space before and after quotation
                ('" ([^\n"]+) "', r'"\1"'),
                (" ([" + punc_after + "])", r"\1"),  # remove space before
                ("([" + punc_before + "]) ", r"\1"),  # remove space after
                # put space after . and :
                (
                    "([" + punc_after[:3] + "])([^ " + punc_after + r"\d۰۱۲۳۴۵۶۷۸۹])",
                    r"\1 \2",
                ),
                (
                    "([" + punc_after[3:] + "])([^ " + punc_after + "])",
                    r"\1 \2",
                ),  # put space after
                (
                    "([^ " + punc_before + "])([" + punc_before + "])",
                    r"\1 \2",
                ),  # put space before
                # put space after number; e.g., به طول ۹متر -> به طول ۹ متر
                (r"(\d)([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])", r"\1 \2"),
                # put space after number; e.g., به طول۹ -> به طول ۹
                (r"([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])(\d)", r"\1 \2"),
            ]

            self.affix_spacing_patterns = [
                (r"([^ ]ه) ی ", r"\1‌ی "),  # fix ی space
                (r"(^| )(ن?می) ", r"\1\2‌"),  # put zwnj after می, نمی
                # put zwnj before تر, تری, ترین, گر, گری, ها, های
                (
                    r"(?<=[^\n\d "
                    + punc_after
                    + punc_before
                    + "]{2}) (تر(ین?)?|گری?|های?)(?=[ \n"
                    + punc_after
                    + punc_before
                    + "]|$)",
                    r"‌\1",
                ),
                # join ام, ایم, اش, اند, ای, اید, ات
                (
                    r"([^ ]ه) (ا(م|یم|ش|ند|ی|ید|ت))(?=[ \n" + punc_after + "]|$)",
                    r"\1‌\2",
                ),
                # شنبهها => شنبه‌ها
                ("(ه)(ها)", r"\1‌\2"),
            ]

        if self._persian_style:
            self.persian_style_patterns = [
                ('"([^\n"]+)"', r"«\1»"),  # replace quotation with gyoome
                (r"([\d+])\.([\d+])", r"\1٫\2"),  # replace dot with momayez
                (r" ?\.\.\.", " …"),  # replace 3 dots
            ]


        if self._remove_diacritics:
            self.diacritics_patterns = [
                # remove FATHATAN, DAMMATAN, KASRATAN, FATHA, DAMMA, KASRA, SHADDA, SUKUN
                ("[\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652]", ""),
            ]

        if self._unicodes_replacement:
            self.replacements = [
                ("﷽", "بسم الله الرحمن الرحیم"),
                ("﷼", "ریال"),
                ("(ﷰ|ﷹ)", "صلی"),
                ("ﷲ", "الله"),
                ("ﷳ", "اکبر"),
                ("ﷴ", "محمد"),
                ("ﷵ", "صلعم"),
                ("ﷶ", "رسول"),
                ("ﷷ", "علیه"),
                ("ﷸ", "وسلم"),
                ("ﻵ|ﻶ|ﻷ|ﻸ|ﻹ|ﻺ|ﻻ|ﻼ", "لا"),
            ]

    def normalize(self: "Normalizer", text: str) -> str:

        translations = maketrans(self.translation_src, self.translation_dst)
        text = text.translate(translations)

        if self._persian_style:
            text = self.persian_style(text)

        if self._persian_number:
            text = self.persian_number(text)

        if self._remove_diacritics:
            text = self.remove_diacritics(text)

        if self._correct_spacing:
            text = self.correct_spacing(text)

        if self._unicodes_replacement:
            text = self.unicodes_replacement(text)
            
        if self._seperate_mi:
            text = self.seperate_mi(text)

        return text

    def correct_spacing(self: "Normalizer", text: str) -> str:

        text = regex_replace(self.extra_space_patterns, text)

        lines = text.split("\n")
        result = []
        for line in lines:
            tokens = self.tokenizer.tokenize(line)
            spaced_tokens = self.token_spacing(tokens)
            line = " ".join(spaced_tokens)
            result.append(line)

        text = "\n".join(result)

        text = regex_replace(self.affix_spacing_patterns, text)
        return regex_replace(self.punctuation_spacing_patterns, text)


    def remove_diacritics(self: "Normalizer", text: str) -> str:

        return regex_replace(self.diacritics_patterns, text)
    
    def persian_style(self: "Normalizer", text: str) -> str:

        return regex_replace(self.persian_style_patterns, text)

    def persian_number(self: "Normalizer", text: str) -> str:

        translations = maketrans(
            self.number_translation_src,
            self.number_translation_dst,
        )
        return text.translate(translations)

    def unicodes_replacement(self: "Normalizer", text: str) -> str:
        for old, new in self.replacements:
            text = re.sub(old, new, text)

        return text

    def seperate_mi(self: "Normalizer", text: str) -> str:

        matches = re.findall(r"\bن?می[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]+", text)
        for m in matches:
            r = re.sub("^(ن?می)", r"\1‌", m)
            if r in self.verbs:
                text = text.replace(m, r)

        return text

    def token_spacing(self: "Normalizer", tokens: List[str]) -> List[str]:

        result = []
        for t, token in enumerate(tokens):
            joined = False

            if result:
                token_pair = result[-1] + "‌" + token
                if (
                    token_pair in self.verbs
                    or token_pair in self.words
                    and self.words[token_pair][0] > 0
                ):
                    joined = True

                    if (
                        t < len(tokens) - 1
                        and token + "_" + tokens[t + 1] in self.verbs
                    ):
                        joined = False

                elif token in self.suffixes and result[-1] in self.words:
                    joined = True

            if joined:
                result.pop()
                result.append(token_pair)
            else:
                result.append(token)

        return result

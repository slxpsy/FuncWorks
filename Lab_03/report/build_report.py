from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageBreak, PageTemplate,
                                Image, Paragraph, Spacer)


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "Звіт_Лабораторна_3_оновлений.pdf"
FONT_DIR = Path(r"C:\Windows\Fonts")
pdfmetrics.registerFont(TTFont("DejaVu", str(FONT_DIR / "times.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(FONT_DIR / "timesbd.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Italic", str(FONT_DIR / "timesi.ttf")))


class Report(BaseDocTemplate):
    def __init__(self, filename: str):
        super().__init__(filename, pagesize=A4, leftMargin=25*mm, rightMargin=25*mm,
                         topMargin=22*mm, bottomMargin=22*mm, title="Звіт з лабораторної роботи №3")
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="body")
        self.addPageTemplates([PageTemplate(id="pages", frames=frame, onPage=self.decorate)])

    @staticmethod
    def decorate(canvas, doc):
        if doc.page > 1:
            canvas.saveState()
            canvas.setFont("DejaVu", 14)
            canvas.setFillColor(colors.HexColor("#777777"))
            canvas.drawCentredString(A4[0] / 2, 12*mm, str(doc.page))
            canvas.restoreState()


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="BodyUA", fontName="DejaVu", fontSize=14, leading=19,
                          alignment=TA_JUSTIFY, spaceAfter=8))
styles.add(ParagraphStyle(name="TitleUA", fontName="DejaVu-Bold", fontSize=14, leading=19,
                          alignment=TA_CENTER, spaceAfter=8))
styles.add(ParagraphStyle(name="HeadingUA", fontName="DejaVu-Bold", fontSize=14, leading=19,
                          spaceBefore=9, spaceAfter=7, keepWithNext=True))
styles.add(ParagraphStyle(name="SubUA", fontName="DejaVu-Bold", fontSize=14, leading=19,
                          spaceBefore=7, spaceAfter=5, keepWithNext=True))
styles.add(ParagraphStyle(name="BulletUA", parent=styles["BodyUA"], leftIndent=16,
                          firstLineIndent=-9, bulletIndent=0, spaceAfter=5))
styles.add(ParagraphStyle(name="Cover", fontName="DejaVu", fontSize=14, leading=20,
                          alignment=TA_CENTER, spaceAfter=4))
styles.add(ParagraphStyle(name="CoverBold", parent=styles["Cover"], fontName="DejaVu-Bold"))
styles.add(ParagraphStyle(name="RightUA", fontName="DejaVu", fontSize=14, leading=20,
                          alignment=TA_RIGHT, spaceAfter=5))
styles.add(ParagraphStyle(name="CodeUA", fontName="DejaVu", fontSize=14, leading=18,
                          leftIndent=12, backColor=colors.HexColor("#F2F4F7"), borderPadding=8,
                          spaceBefore=3, spaceAfter=8))
styles.add(ParagraphStyle(name="FigureCaption", fontName="DejaVu-Bold", fontSize=14, leading=19,
                          alignment=TA_CENTER, spaceAfter=10))


def p(text: str, style: str = "BodyUA") -> Paragraph:
    return Paragraph(text, styles[style])


def bullet(text: str) -> Paragraph:
    return Paragraph("•&nbsp;&nbsp;" + text, styles["BulletUA"])


def screenshot(filename: str, caption: str) -> list:
    path = Path(__file__).resolve().parent / "screenshots" / filename
    width_px, height_px = ImageReader(str(path)).getSize()
    draw_width = 160 * mm
    draw_height = draw_width * height_px / width_px
    max_height = 185 * mm
    if draw_height > max_height:
        draw_height = max_height
        draw_width = draw_height * width_px / height_px
    return [p(caption, "FigureCaption"), Image(str(path), width=draw_width, height=draw_height), PageBreak()]


story = []
story += [Spacer(1, 3*mm), p("МІНІСТЕРСТВО ОСВІТИ І НАУКИ УКРАЇНИ<br/>ЛЬВІВСЬКИЙ НАЦІОНАЛЬНИЙ УНІВЕРСИТЕТ ІМЕНІ ІВАНА ФРАНКА", "Cover")]
story += [p("Факультет електроніки та комп’ютерних технологій", "Cover"), Spacer(1, 19*mm)]
story += [p("Звіт", "CoverBold"), p("З ЛАБОРАТОРНОЇ РОБОТИ №3", "Cover"),
          p("Варіант 12", "Cover"), p('на тему: <b>"Незмінні структури даних у Python"</b>', "Cover")]
story += [Spacer(1, 48*mm)]
story += [p("Виконав:<br/>Студент групи ФЕП-22<br/><b>Сисак Ілля</b>", "RightUA"), Spacer(1, 8*mm)]
story += [p("Перевірив:<br/>Аспірант<br/><b>Остріков Данило Андрійович</b>", "RightUA")]
story += [Spacer(1, 34*mm), p("Львів 2026", "CoverBold"), PageBreak()]

story += [p("Мета роботи", "HeadingUA"),
          p("Застосувати незмінні структури даних у Python на прикладі предметної області «Ресторанне меню» (варіант 12). Перенести модель на frozen dataclasses, tuple, frozenset і MappingProxyType; замінити мутації чистими оновленнями та оцінити їх тестами й вимірюванням часу."),
          p("Основні поняття", "HeadingUA"),
          bullet("<b>Незмінність</b> — стан об’єкта після створення не змінюється; оновлення повертає новий об’єкт."),
          bullet("<b>Чиста функція</b> залежить від переданих аргументів і не змінює зовнішній стан."),
          bullet("<b>MappingProxyType</b> надає режим лише читання; для ізоляції від змін джерела перед створенням proxy робиться копія."),
          p("Хід роботи", "HeadingUA"),
          p("Проєкт побудований модульно за зразком попередньої лабораторної: модель, чисте ядро, CLI-оболонка, точка входу та тести."),
          p("Проєктування моделі (model.py)", "SubUA")]
story += [
          bullet("<b>Ingredient</b> і <b>Dish</b> реалізовано як @dataclass(frozen=True, slots=True); перевіряються назви, ціни, кількості та типи колекцій."),
          bullet("Інгредієнти зберігаються в tuple, алергени — у frozenset, метадані копіюються й обгортаються MappingProxyType."),
          bullet("Ingredient хешується, бо його поля незмінні. Dish навмисно не є хешованим через MappingProxyType; це обмеження задокументоване тестом."), PageBreak()]
story += screenshot("01_model.png", "Рисунок 1 — Незмінні моделі Ingredient і Dish (model.py)")

story += [p("Реалізація чистих оновлень (core.py)", "HeadingUA"),
          bullet("add_ingredient() і remove_ingredient() створюють новий tuple складників."),
          bullet("add_allergen() застосовує об’єднання frozenset, а with_price() повертає нову ціну."),
          bullet("discounted() розраховує нову ціну без зміни початкової страви; некоректний відсоток відхиляється."),
          bullet("filter_by_allergen() відбирає позиції без побічних ефектів."),
          bullet("freeze() рекурсивно копіює Mapping у read-only proxy, списки/кортежі в tuple, а множини у frozenset."),
          Spacer(1, 2*mm)]
story += screenshot("02_core.png", "Рисунок 2 — Чисті функції оновлення меню (core.py)")

story += [p("Інтерфейс і запуск", "HeadingUA"),
          p("Модуль app.py формує демонстраційне меню та текстовий звіт. main.py надає CLI з необов’язковим параметром --allergen для фільтрування меню. benchmark.py порівнює копіювання змінних dict/set зі створенням оновлення frozen-моделі."),
          p("Приклад запуску", "SubUA"),
          p("python main.py<br/>python main.py --allergen молоко<br/>python -m pytest -q --durations=5<br/>python benchmark.py", "CodeUA"),
          p("Тестування (tests/test_core.py)", "HeadingUA"),
          bullet("Тести перевіряють, що додавання/видалення інгредієнтів, алергенів і зміна ціни не змінюють оригінал."),
          bullet("Окремо тестується read-only поведінка метаданих і копіювання вхідного словника."),
          bullet("Також покрито валідацію, рекурсивне freeze, хешованість Ingredient і очікувану нехешованість Dish.")]
story += [PageBreak()]
story += screenshot("03_tests_updates.png", "Рисунок 3 — Тести чистих оновлень без мутацій")
story += screenshot("04_tests_metadata.png", "Рисунок 4 — Тести алергенів, ціни, метаданих і frozen-моделі")

story += [p("Вимірювання продуктивності", "HeadingUA"),
          p("benchmark.py виконує по 20 000 оновлень сім разів і виводить медіану часу для mutable та immutable варіантів. Це дає змогу порівняти накладні витрати копіювання на цій машині; вимірювання не є універсальним для інших середовищ. Фактичні значення з’являться після запуску скрипту.")]
story += screenshot("05_benchmark.png", "Рисунок 5 — Порівняння benchmark mutable та immutable оновлень")

story += [p("Висновки", "HeadingUA"),
          p("У лабораторній роботі модель ресторанного меню переведено на незмінні структури Python. Дві доменні сутності реалізовані frozen dataclasses; колекції інгредієнтів та алергенів представлені tuple і frozenset, а словникові метадані захищені копією з MappingProxyType."),
          p("Операції додавання/видалення інгредієнтів, позначення алергенів, оновлення ціни й застосування знижки повертають нові страви, зберігаючи вихідний стан. Реалізовано рекурсивне заморожування вкладених колекцій, фільтрацію меню, набір pytest-тестів та скрипт вимірювання часу."),
          p("Незмінність спрощує відтворення стану й перевірку функцій, зменшує ризик прихованих побічних ефектів. Її ціна — створення нових об’єктів і копіювання колекцій під час оновлення. MappingProxyType також означає, що Dish не можна використати як ключ словника без окремого хешованого представлення; це враховано в моделі й тестах."),
          Spacer(1, 8*mm), p("До проєкту додані конфігурації pytest, mypy, black і ruff. README містить команди запуску та короткий аналіз компромісу між надійністю й витратами на копіювання.")]

Report(str(OUT)).build(story)
print(OUT)

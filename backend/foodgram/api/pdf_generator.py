import io

from django.conf import settings

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.rl_config import TTFSearchPath

from recipes.models import RecipeIngredient

TTFSearchPath.append(
    str(settings.BASE_DIR) + '/data/reportlabs/fonts')


class PdfGenerator:

    def __init__(self, user):
        self.user = user

    def generate(self):
        shopping_cart = {}
        recipes = self.user.shopping_cart.all()
        data = RecipeIngredient.objects.filter(recipe__in=recipes)
        for recipe_ingredient in data:
            ingredient_name = recipe_ingredient.ingredient.name
            measurement_unit = recipe_ingredient.ingredient.measurement_unit
            amount = recipe_ingredient.amount
            if ingredient_name in shopping_cart.keys():
                shopping_cart[ingredient_name][0] += amount
            else:
                shopping_cart[ingredient_name] = [amount, measurement_unit]

        buf = io.BytesIO()
        pdf_canvas = canvas.Canvas(buf, pagesize=letter, bottomup=0)

        textob = pdf_canvas.beginText(40, 680)
        textob.setTextOrigin(inch, inch)
        pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
        textob.setFont('FreeSans', 14)

        lines = []

        lines.append('Список покупок:')
        lines.append('')
        for ingredient_name, amount_data in shopping_cart.items():
            lines.append(
                f'{ingredient_name}: {amount_data[0]} {amount_data[1]}')

        for line in lines:
            textob.textLines(line)

        pdf_canvas.drawText(textob)
        pdf_canvas.showPage()
        pdf_canvas.save()
        buf.seek(0)

        return buf

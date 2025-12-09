from modeltranslation.translator import register, TranslationOptions
from .models import Category,Product
from .models import ProductQuestion, ProductQuestionOption

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', )  # hangi alanların çevirisini istiyorsan buraya yaz




@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'features', 'description', 'warranty_period')


@register(ProductQuestion)
class ProductQuestionTranslationOptions(TranslationOptions):
    fields = ('question_text',)

@register(ProductQuestionOption)
class ProductQuestionOptionTranslationOptions(TranslationOptions):
    fields = ('option_text',)



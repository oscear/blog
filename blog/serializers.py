# serializersapi.py
from rest_framework import serializers
from .models import Article


#序列化：程序中的一个数据结构类型转换为其他格式（字典、JSON、XML等），例如将Django中的模型类对象装换为JSON字符串
#反序列化：将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'#默认序列化全部
        #fields = ('id', 'name', 'mail', 'create_time')  指定序列化字段，将fileds设置为元组
        #exclude = ('id', 'sex', 'age')   排除模式
        # 添加选项参数，extra_kwargs = {
        #     'readcount' : {'min_value': 0,'max_value': 999,'required':True },
        #     'commet' : {'min_value': 0,'max_value': 999,'required':True },
        # }

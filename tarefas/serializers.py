from rest_framework import serializers

from .models import Tarefa


class TarefaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefa
        fields = '__all__'
        # O dono vem sempre do token (request.user), nunca do corpo da requisição.
        extra_kwargs = {'usuario': {'read_only': True}}
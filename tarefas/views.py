from rest_framework import generics
from .models import Tarefa
from .serializers import TarefaSerializer

class TarefaListCreateView(generics.ListCreateAPIView):
    serializer_class = TarefaSerializer

    def get_queryset(self):
        # Isolamento: só as tarefas de quem fez a requisição.
        queryset = Tarefa.objects.filter(usuario=self.request.user)

        # Filtro opcional ?concluida=true|false
        concluida = self.request.query_params.get('concluida')
        if concluida is not None:
            queryset = queryset.filter(concluida=(concluida.lower() == 'true'))

        # Filtro opcional ?prioridade=alta|media|baixa
        prioridade = self.request.query_params.get('prioridade')
        if prioridade:
            queryset = queryset.filter(prioridade=prioridade.upper())

        return queryset

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class TarefaDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TarefaSerializer

    def get_queryset(self):
        # Tarefa de outro usuário não está no queryset: a API responde 404.
        return Tarefa.objects.filter(usuario=self.request.user)
# Tests have been moved to the tests/ directory.
        self.assertIsNotNone(task.completed_at)

        task.completed = False
        task.save()
        self.assertIsNone(task.completed_at)


class TaskViewsIntegrationTests(TestCase):
    def test_listagem_de_tarefas(self):
        Task.objects.create(title="Tarefa A", description="desc", completed=False)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tarefa A")

    def test_criacao_de_tarefa(self):
        response = self.client.post(
            "/tasks/",
            {
                "title": "Nova Tarefa",
                "description": "desc",
                "completed": False,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title="Nova Tarefa").exists())

    def test_edicao_de_tarefa(self):
        task = Task.objects.create(title="Editar", description="desc", completed=False)

        response = self.client.post(
            f"/tasks_update/{task.id}",
            {
                "title": "Editada",
                "description": "desc 2",
                "completed": True,
            },
        )
        self.assertEqual(response.status_code, 302)

        task.refresh_from_db()
        self.assertEqual(task.title, "Editada")
        self.assertTrue(task.completed)
        self.assertIsNotNone(task.completed_at)

    def test_remocao_de_tarefa(self):
        task = Task.objects.create(title="Excluir", description="desc", completed=False)

        response = self.client.get(f"/tasks_delete/{task.id}")
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=task.id).exists())


class AnaliseProdutividadeTests(TestCase):
    def test_tarefas_por_dia(self):
        df = pd.DataFrame(
            {
                "created_at": [
                    "2026-02-01 10:00:00",
                    "2026-02-01 12:00:00",
                    "2026-02-02 09:00:00",
                ]
            }
        )

        resultado = tarefas_por_dia(df)
        self.assertEqual(len(resultado), 2)
        self.assertEqual(int(resultado.loc[0, "tarefas_criadas"]), 2)
        self.assertEqual(int(resultado.loc[1, "tarefas_criadas"]), 1)

    def test_media_tempo_conclusao(self):
        df = pd.DataFrame(
            {
                "created_at": ["2026-02-01 10:00:00", "2026-02-01 12:00:00"],
                "completed_at": ["2026-02-01 12:00:00", "2026-02-01 16:00:00"],
            }
        )

        media = media_tempo_conclusao(df)
        self.assertEqual(media, pd.Timedelta(hours=3))

    def test_media_tempo_conclusao_sem_dados(self):
        df = pd.DataFrame({"created_at": ["2026-02-01 10:00:00"], "completed_at": [None]})
        media = media_tempo_conclusao(df)
        self.assertIsNone(media)

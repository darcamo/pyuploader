
from app.models import *
from datetime import date


def fill_users():
    if db.session.query(User).count() > 0:
        print("Usuários já foram adicionados antes")
        return
    else:
        u = User(username="darlan", name="Darlan Cavalcante Moreira",
                 password="221282", superuser=True)
        db.session.add(u)
        db.session.commit()

        with open('Lista_de_Alunos_3A.txt') as f:
            for line in f:
                matricula, nome = line.replace('\n', '').split(',')
                nome = nome.title()
                u = User(username=matricula, name=nome,
                         password=matricula, superuser=False)
                db.session.add(u)
                # print('{0}: {1}'.format(matricula, nome))

        with open('Lista_de_Alunos_3B.txt') as f:
            for line in f:
                matricula, nome = line.replace('\n', '').split(',')
                nome = nome.title()
                u = User(username=matricula, name=nome,
                         password=matricula, superuser=False)
                db.session.add(u)
                # print('{0}: {1}'.format(matricula, nome))

        # Commit all changes
        db.session.commit()


def fill_trabalhos():
    if db.session.query(Trabalhos).count() > 0:
        print("Trabalhos já foram adicionados antes")
        return
    else:
        startdate1 = date(year=2016, month=4, day=19)
        deadline1 = date(year=2016, month=4, day=26)
        startdate2 = date(year=2016, month=4, day=26)
        deadline2 = date(year=2016, month=5, day=3)
        startdate3 = date(year=2016, month=5, day=26)
        deadline3 = date(year=2016, month=6, day=26)
        t1 = Trabalhos(name="Pratica 1", type="Pratica",
                       startdate=startdate1, deadline=deadline1, em_aberto=False)
        t2 = Trabalhos(name="Pratica 2", type="Pratica",
                       startdate=startdate2, deadline=deadline2)
        t3 = Trabalhos(name="Trabalho 1", type="Trabalho",
                       startdate=startdate3, deadline=deadline3)
        db.session.add_all([t1, t2, t3])
        db.session.commit()


def fill_trabalhos_entregues():
    if db.session.query(TrabalhoEntregue).count() > 0:
        print("Trabalhos entregues já foram adicionados antes")
        return
    else:
        trabalhos = db.session.query(Trabalhos).all()
        alunos = db.session.query(User).all()
        t1 = TrabalhoEntregue(trabalho_id=trabalhos[0].id,
                              user_id=alunos[0].id,
                              path="/home/lala/file.zip",
                              entrega=datetime.today())
        t2 = TrabalhoEntregue(trabalho_id=trabalhos[1].id,
                              user_id=alunos[0].id,
                              path="/home/lele/file.zip",
                              entrega=datetime.today())
        db.session.add(t1)
        db.session.add(t2)

        t2 = TrabalhoEntregue(trabalho_id=trabalhos[1].id,
                              user_id=alunos[1].id,
                              path="/home/hehe/file.zip",
                              entrega=datetime.today())
        db.session.add(t2)
        db.session.commit()

# xxxxxxxxxx Main xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
if __name__ == '__main__':
    fill_users()
    fill_trabalhos()
    fill_trabalhos_entregues()

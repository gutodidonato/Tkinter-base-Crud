import tkinter as tk
import cx_Oracle
import json
from tkinter import ttk

with open("bloco.json") as file:
    data = json.load(file)
    hostname = data["hostname"]
    port = data["port"]
    sid = data["sid"]
    username = data["username"]
    password = data["password"]

dsn_tns = cx_Oracle.makedsn(hostname, port, sid)
connection = cx_Oracle.connect(username, password, dsn_tns)


def listar():
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM EMPRESAS_RED ORDER BY PRIORIDADE ASC"
        cursor.execute(query)
        for row in cursor:
            print(row)
    finally:
        cursor.close()
        connection.close()


def atribuir(pessoa, id_empresa):
    try:
        cursor = connection.cursor()
        query = (
            "update EMPRESAS_RED set pessoa = :pessoa where id_empresa = :id_empresa"
        )
        cursor.execute(query, (pessoa, id_empresa))
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def alterar_descricao(descricao, id_empresa):
    try:
        cursor = connection.cursor()
        query = "update EMPRESAS_RED set descricao = :descricao where id_empresa = :id_empresa"
        cursor.execute(query, (descricao, id_empresa))
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def alterar_prioridade(prioridade, id_empresa):
    try:
        cursor = connection.cursor()
        query = "update EMPRESAS_RED set prioridade = :prioridade where id_empresa = :id_empresa"
        cursor.execute(query, (prioridade, id_empresa))
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def inserir_empresa(prioridade, pessoa, descricao):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT NEXTVAL('EMPRESAS_RED_ID_SEQ')")
        next_id = cursor.fetchone()[0]
        query = "INSERT INTO EMPRESAS_RED (ID_EMPRESA, PRIORIDADE, PESSOA, DESCRICAO) VALUES (:id_empresa, :prioridade, :pessoa, :descricao)"
        cursor.execute(query, (next_id, prioridade, pessoa, descricao))
        connection.commit()

    except cx_Oracle.DatabaseError as e:
        (error,) = e.args
        print("Erro:", error.message)
        connection.rollback()


# GUI

root = tk.Tk()
root.title("Gerenciamento de Empresas")


def listar_empresas():
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM EMPRESAS_RED"
        cursor.execute(query)
        data_tree.delete(*data_tree.get_children())

        all_data = cursor.fetchall()
        for row in all_data:
            data_tree.insert("", tk.END, values=row, tag="l")

    except cx_Oracle.DatabaseError as e:
        (error,) = e.args
        print("Erro:", error.message)


data_frame = tk.Frame(root)
data_frame.grid()


priority_label = tk.Label(data_frame, text="Nome Empresa:")
priority_label.grid(row=1, column=0)
priority_entry = tk.Entry(data_frame)
priority_entry.grid(row=1, column=1)

priority_label = tk.Label(data_frame, text="Prioridade:")
priority_label.grid(row=2, column=0)
priority_entry = tk.Entry(data_frame)
priority_entry.grid(row=2, column=1)


person_label = tk.Label(data_frame, text="Pessoa:")
person_label.grid(row=3, column=0)
person_entry = tk.Entry(data_frame)
person_entry.grid(row=3, column=1)


description_label = tk.Label(data_frame, text="Descrição:")
description_label.grid(row=4, column=0)
description_entry = tk.Text(data_frame, height=2)
description_entry.grid(row=4, column=1)

# Buttons for operations
button_frame = tk.Frame(root)
button_frame.grid()

insert_button = tk.Button(button_frame, text="Inserir")
insert_button.grid(row=6, column=0)

update_button = tk.Button(button_frame, text="Atualizar")
update_button.grid(row=6, column=1)

listar_button = tk.Button(button_frame, text="Listar", command=listar_empresas)
listar_button.grid(row=6, column=2)

delete_button = tk.Button(button_frame, text="Excluir")
delete_button.grid(row=6, column=3)


data_tree = ttk.Treeview(
    data_frame, columns=("ID", "Empresa", "Prioridade", "Pessoa", "Descrição")
)
data_tree.heading("ID", text="ID")
data_tree.heading("Empresa", text="Empresa")
data_tree.heading("Prioridade", text="Prioridade")
data_tree.heading("Pessoa", text="Pessoa")
data_tree.heading("Descrição", text="Descrição")

data_tree.column("ID", width=50)
data_tree.column("Empresa", width=150)
data_tree.column("Prioridade", width=100)
data_tree.column("Pessoa", width=150)
data_tree.column("Descrição", width=200)
data_tree.grid(row=6, column=1)


listar_empresas()

root.mainloop()

import streamlit as st
import pandas as pd
from datetime import date

import storage


def main():
    st.title("Assistente Financeiro Pessoal")

    storage.init_db()

    menu = st.sidebar.selectbox("Navegação", ["Transações", "Resumo", "Metas"])

    if menu == "Transações":
        st.header("Registrar transação")
        with st.form("tx_form"):
            tx_date = st.date_input("Data", value=date.today())
            tx_type = st.selectbox("Tipo", ["expense", "income"]) 
            category = st.text_input("Categoria")
            amount = st.number_input("Valor", format="%.2f")
            note = st.text_area("Observação")
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                storage.add_transaction(tx_date, tx_type, category, float(amount), note)
                st.success("Transação adicionada")

        st.header("Transações recentes")
        rows = storage.list_transactions()
        if rows:
            df = pd.DataFrame(rows)
            df["date"] = pd.to_datetime(df["date"]).dt.date
            st.dataframe(df)
        else:
            st.info("Nenhuma transação registrada")

    elif menu == "Resumo":
        st.header("Resumo financeiro")
        s = storage.get_summary()
        st.metric("Receitas", f"R$ {s['income']:.2f}")
        st.metric("Despesas", f"R$ {s['expense']:.2f}")
        st.metric("Saldo", f"R$ {s['balance']:.2f}")

    else:
        st.header("Metas")
        with st.form("goal_form"):
            name = st.text_input("Nome da meta")
            target = st.number_input("Valor alvo", format="%.2f")
            no_due = st.checkbox("Sem prazo")
            if no_due:
                due = None
            else:
                due = st.date_input("Prazo", value=date.today())
            addg = st.form_submit_button("Criar meta")
            if addg:
                storage.add_goal(name, float(target), due)
                st.success("Meta criada")

        st.info("Funcionalidade de metas simples criada.")


if __name__ == "__main__":
    main()

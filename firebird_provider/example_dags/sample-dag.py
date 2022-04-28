#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
This is an example DAG for the use of the FirebirdOperator.
In this example, we create two tasks that execute in sequence.
The first task calls an sql command, defined in the SQLite operator,
which when triggered, is performed on the connected firebird database.
The second task is similar but instead calls the SQL command from an external file.
"""

from datetime import datetime

from airflow import DAG
from airflow.providers.firebird.hooks.firebird import FirebirdHook
from airflow.providers.firebird.operators.firebird import FirebirdOperator

dag = DAG(
    dag_id='example_firebird',
    schedule_interval='@daily',
    start_date=datetime(2021, 1, 1),
    tags=['example'],
    catchup=False,
)

# [START howto_operator_firebird]

# Example of creating a task that calls a common CREATE TABLE sql command.
create_table_firebird_task = FirebirdOperator(
    task_id='create_table_firebird',
    sql=r"""
    CREATE TABLE Customers (
        customer_id INT PRIMARY KEY,
        first_name TEXT,
        last_name TEXT
    );
    """,
    dag=dag,
)

# [END howto_operator_firebird]


@dag.task(task_id="insert_firebird_task")
def insert_firebird_hook():
    firebird_hook = FirebirdHook()

    rows = [('James', '11'), ('James', '22'), ('James', '33')]
    target_fields = ['first_name', 'last_name']
    firebird_hook.insert_rows(table='Customers', rows=rows, target_fields=target_fields)


@dag.task(task_id="replace_firebird_task")
def replace_firebird_hook():
    firebird_hook = FirebirdHook()

    rows = [('James', '11'), ('James', '22'), ('James', '33')]
    target_fields = ['first_name', 'last_name']
    firebird_hook.insert_rows(table='Customers', rows=rows, target_fields=target_fields, replace=True)


# [START howto_operator_firebird_external_file]

# Example of creating a task that calls an sql command from an external file.
external_create_table_firebird_task = FirebirdOperator(
    task_id='create_table_firebird_external_file',
    sql='create_table.sql',
)

# [END howto_operator_firebird_external_file]

create_table_firebird_task >> external_create_table_firebird_task >> insert_firebird_hook() >> replace_firebird_hook()

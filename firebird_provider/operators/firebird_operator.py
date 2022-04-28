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
from typing import Any, Iterable, List, Mapping, Optional, Sequence, Union

from airflow.models import BaseOperator
from airflow.providers.firebird.hooks.firebird import FirebirdHook


class FirebirdOperator(BaseOperator):
    """
    Executes sql code in a specific firebird database

    .. seealso::
        For more information on how to use this operator, take a look at the guide:
        :ref:`howto/operator:FirebirdOperator`

    :param sql: the sql code to be executed. Can receive a str representing a
        sql statement, a list of str (sql statements), or reference to a template file.
        Template reference are recognized by str ending in '.sql'
        (templated)
    :param firebird_conn_id: reference to a specific firebird database
    :param parameters: (optional) the parameters to render the SQL query with.
    """

    template_fields: Sequence[str] = ('sql',)
    template_ext: Sequence[str] = ('.sql',)
    template_fields_renderers = {'sql': 'sql'}
    ui_color = '#E82020'

    def __init__(
        self,
        *,
        sql: Union[str, List[str]],
        firebird_conn_id: str = 'firebird_default',
        parameters: Optional[Union[Mapping, Iterable]] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.firebird_conn_id = firebird_conn_id
        self.sql = sql
        self.parameters = parameters or []

    def execute(self, context: Mapping[Any, Any]) -> None:
        self.log.info('Executing: %s', self.sql)
        hook = FirebirdHook(firebird_conn_id=self.firebird_conn_id)
        hook.run(self.sql, parameters=self.parameters)

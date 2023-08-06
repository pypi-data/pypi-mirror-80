#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Active active AAP

Revision ID: b76dc22f2e23
Revises: 24427b3a5c95
Create Date: 2019-11-21 14:18:11.909757

"""

# revision identifiers, used by Alembic.
revision = 'b76dc22f2e23'
down_revision = '24427b3a5c95'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('apic_aim_subnet_extensions',
                  sa.Column('active_active_aap', sa.Boolean,
                            server_default=sa.false(), nullable=False))


def downgrade():
    pass

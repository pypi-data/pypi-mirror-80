from typing import List

from spintop.models import BaseDataClass, DeprecatedBy, get_serializer

class OrgDataEnv(BaseDataClass):
    vars: dict = dict
    name: str

class Organization(BaseDataClass):
    key: str
    project_id: str
    envs: List[OrgDataEnv] = list

    def find_env(self, env_name):
        for env in self.envs:
            if env.name == env_name:
                return env
        else:
            raise ValueError(f'Org {org_key} has no env named {env_name}')

    def env_dataset_name(self, env_name):
        return f'data__{self.key}__{env_name}'

class ManyOrganizations(BaseDataClass):
    orgs: List[Organization]

    def __iter__(self):
        return iter(self.orgs)
    
    def find_org(self, org_key):
        for org in self.orgs:
            if org.key == org_key:
                return org
        else:
            raise ValueError(f'No org named {org_key}')
    

class User(BaseDataClass):
    username: str = None
    user_id: str
    scope: List[str]
    permissions: List[str]
    user_type: str
    organizations: List[Organization]

from abc import ABC

from ad_import.load_data import LoadAd
from ad_import.models import Computer


class LoadComputers(LoadAd, ABC):
    fields = ['cn',
              'description',
              'distinguishedName',
              'lastLogon',
              'logonCount',
              'name',
              'objectGUID',
              'objectSid',
              'operatingSystem',
              'operatingSystemHotfix',
              'operatingSystemServicePack',
              'operatingSystemVersion',
              'pwdLastSet',
              'userAccountControl',
              'whenChanged',
              'whenCreated',
              ]

    model = Computer

    def load(self, query):
        entries = self.run_query(query)
        for user_data in entries:
            computer: Computer
            computer, exist = self.get_object(user_data)

            computer.cn = user_data.string('cn')
            computer.description = user_data.string('description')
            computer.distinguishedName = user_data.string('distinguishedName')
            computer.lastLogon = user_data.date('lastLogon')
            computer.logonCount = user_data.numeric('logonCount')
            computer.name = user_data.string('name')
            computer.objectGUID = user_data.bytes('objectGUID')
            computer.objectSid = user_data.bytes('objectSid')
            computer.operatingSystem = user_data.string('operatingSystem')
            computer.operatingSystemHotfix = user_data.string('operatingSystemHotfix')
            computer.operatingSystemServicePack = user_data.string('operatingSystemServicePack')
            computer.operatingSystemVersion = user_data.string('operatingSystemVersion')
            computer.pwdLastSet = user_data.date('pwdLastSet')
            computer.userAccountControl = user_data.numeric('userAccountControl')
            computer.whenChanged = user_data.date_string('whenChanged')
            computer.whenCreated = user_data.date_string('whenCreated')

            if computer.disabled() and not exist:
                print('%s is disabled' % computer)
            else:
                computer.save()

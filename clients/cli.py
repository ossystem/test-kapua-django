from clients.models import Client, Domain


tenant = Client(schema_name='public',
                name='default',
                active=True)
tenant.save()

domain = Domain()
domain.domain = 'kapua' # don't add your port or www here!
domain.tenant = tenant
domain.is_primary = True
domain.save()


tenant = Client(schema_name='tenant1',
                name='Tenant1',
                active=True)
tenant.save()

domain = Domain()
domain.domain = 'tenant1.kapua' # don't add your port or www here!
domain.tenant = tenant
# domain.is_primary = True
domain.save()


tenant = Client(schema_name='tenant2',
                name='Tenant2',
                active=True)
tenant.save()

domain = Domain()
domain.domain = 'tenant2.kapua' # don't add your port or www here!
domain.tenant = tenant
# domain.is_primary = True
domain.save()
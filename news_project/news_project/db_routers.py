
class ProductionRouter:
    def db_for_read(self, model, **hints):
        """Directs read operations for `ProductionApNewsModel` to `production_db`."""
        if model._meta.db_table == 'production_ap_news':
            return 'production_db'
        return 'default'

    def db_for_write(self, model, **hints):
        """Directs write operations for `ProductionApNewsModel` to `production_db`."""
        if model._meta.db_table == 'production_ap_news':
            return 'production_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """Allows relations between models within `default` and `production_db`."""
        if obj1._state.db in ['default', 'production_db'] and obj2._state.db in ['default', 'production_db']:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Controls where migrations are allowed based on app_label and model_name."""
        if model_name == 'productionapnewsmodel':
            return db == 'production_db'
        return db == 'default'
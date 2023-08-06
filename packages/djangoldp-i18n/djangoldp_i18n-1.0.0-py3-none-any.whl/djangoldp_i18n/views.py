from djangoldp.views import LDPViewSet
from djangoldp_i18n.serializers import I18nLDPSerializer, I18nContainerSerializer


class I18nLDPViewSet(LDPViewSet):
    '''
    Overrides LDPViewSet to use custom serializer
    '''

    def build_serializer(self, meta_args, name_prefix):
        meta_args['list_serializer_class'] = I18nContainerSerializer
        meta_class = type('Meta', (), meta_args)

        return type(I18nLDPSerializer)(self.model._meta.object_name.lower() + name_prefix + 'Serializer',
                                       (I18nLDPSerializer,),{'Meta': meta_class})
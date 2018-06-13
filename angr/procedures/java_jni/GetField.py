from . import JNISimProcedure

from ...engines.soot.values import SimSootValue_InstanceFieldRef

import logging
l = logging.getLogger('angr.procedures.java_jni.getfield')

class GetField(JNISimProcedure):

    return_ty = None

    def run(self, ptr_env, obj_, field_id_):

        # lookup parameter
        obj = self.state.jni_references.lookup(obj_)
        tmp_field_id = self.state.jni_references.lookup(field_id_)

        # update field with info of the actual object (=> add heap_alloc_id)
        field_id = SimSootValue_InstanceFieldRef(heap_alloc_id=obj.heap_alloc_id, 
                                                 class_name=tmp_field_id.class_name,
                                                 field_name=tmp_field_id.field_name,
                                                 type_=tmp_field_id.type)

        # load value from java memory
        javavm_memory = self.state.get_javavm_view_of_plugin('memory')
        return javavm_memory.load(field_id)

class GetBooleanField(GetField):
    return_ty = 'boolean'

class GetByteField(GetField):
    return_ty = 'byte'

class GetCharField(GetField):
    return_ty = 'char'

class GetShortField(GetField):
    return_ty = 'short'

class GetIntField(GetField):
    return_ty = 'int'

class GetLongField(GetField):
    return_ty = 'long'

class GetObjectField(GetField):
    return_ty = 'reference'
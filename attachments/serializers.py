# from rest_framework import serializers
# from django.contrib.contenttypes.models import ContentType
# from applicants.models import ApplicantProfile
# from .models import Attachment, ATTACHMENT_TYPE


# class AttachmentCreateSerializer(serializers.ModelSerializer):
#     content_type = serializers.CharField(write_only=True)

#     class Meta:
#         model = Attachment
#         fields = ("content_type", "object_id", "attachment_file", "attachment_type")

#     # def validate(self, data):
#     #     # Validate content_type and object_id combination
#     #     content_type_str = data.get("content_type")
#     #     object_id = data.get("object_id")
#     #     if not (content_type_str and object_id):
#     #         raise serializers.ValidationError("Both content_type and object_id are required.")
#     #     try:
#     #         content_type = ContentType.objects.get(model=content_type_str.lower())
#     #         model_class = content_type.model_class()
#     #         print(model_class)
#     #         if not model_class.objects.filter(id=object_id).exists():
#     #             raise serializers.ValidationError("Invalid object_id provided.")
        
#     #     except ContentType.DoesNotExist:
#     #         raise serializers.ValidationError("Invalid content_type provided.")

#     #     # Ensure the object exists
#     #     model_class = content_type.model_class()
#     #     print(model_class)
#     #     if not model_class.objects.filter(id=object_id).exists():
#     #         raise serializers.ValidationError("Invalid object_id provided.")

#     #     data["content_type"] = content_type
#     #     return data

#         def validate(self, data):
#             # import pdb;pdb.set_trace()
#             content_type = data.get("content_type")
#             object_id = data.get("object_id")
            
#             if not (content_type and object_id):
#                 raise serializers.ValidationError("Both content_type and object_id are required.")

#             try:
#                 # If content_type is an ID, get the ContentType instance
#                 if content_type.isdigit():
#                     content_type_obj = ContentType.objects.get(id=int(content_type))
#                 else:
#                     # If it's a string model name, get the ContentType instance
#                     content_type_obj = ContentType.objects.get(model=content_type.lower())
                
#                 # Get the model class
#                 model_class = content_type_obj.model_class()
                
#                 # Verify that the object exists
#                 model_class.objects.get(pk=object_id)

#                 # Replace the string content_type with the actual ContentType object
#                 data['content_type'] = content_type_obj
#             except ContentType.DoesNotExist:
#                 raise serializers.ValidationError("Invalid content_type provided.")
#             except AttributeError:
#                 raise serializers.ValidationError("Invalid content_type format.")
#             except model_class.DoesNotExist:
#                 raise serializers.ValidationError("Object with given ID does not exist.")

#             return data

#     def create(self, validated_data):
#         # Retrieve content_type object based on the provided string
#         content_type_str = validated_data.pop("content_type")
#         content_type = ContentType.objects.get_for_model(content_type_str)

#         # Create the attachment instance
#         return Attachment.objects.create(
#             content_type=content_type,
#             object_id=validated_data["object_id"],
#             **validated_data,
#         )


from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Attachment, ATTACHMENT_TYPE

class AttachmentCreateSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(write_only=True)

    class Meta:
        model = Attachment
        fields = ("content_type", "object_id", "attachment_file", "attachment_type")

    def validate(self, data):
        content_type = data.get("content_type")
        object_id = data.get("object_id")
        
        if not (content_type and object_id):
            raise serializers.ValidationError("Both content_type and object_id are required.")

        try:
            if content_type.isdigit():
                content_type_obj = ContentType.objects.get(id=int(content_type))
            else:
                content_type_obj = ContentType.objects.get(model=content_type.lower())
            
            model_class = content_type_obj.model_class()
            model_class.objects.get(pk=object_id)

            data['content_type'] = content_type_obj
        except ContentType.DoesNotExist:
            raise serializers.ValidationError("Invalid content_type provided.")
        except model_class.DoesNotExist:
            raise serializers.ValidationError("Object with given ID does not exist.")

        return data

    def create(self, validated_data):
        content_type = validated_data.pop("content_type")
        return Attachment.objects.create(
            content_type=content_type,
            **validated_data,
        )


    
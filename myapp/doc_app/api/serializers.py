from rest_framework import serializers
from doc_app.models import Assignment
from doc_app.models import CustomUser

class AssignmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Assignment
        #doc url 
        
        fields = '__all__' # Include 'id' to help with retrieval

    def validate_doc(self, value):
        # Validate the file extension
        allowed_extensions = ['.pptx', '.docx', '.xlsx', '.pdf']
        if not any(value.name.endswith(ext) for ext in allowed_extensions):
            raise serializers.ValidationError('File type is not allowed. Only pptx, docx, xlsx, and pdf are accepted.')
        return value
    


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    user_type = serializers.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'user_type']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'message': 'Passwords must match'})
        if CustomUser.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'message': 'Email already exists'})

        account = CustomUser(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            user_type=self.validated_data['user_type']
        )
        account.set_password(password)
        account.save()
        return account


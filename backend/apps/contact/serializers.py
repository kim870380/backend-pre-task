from rest_framework import serializers
from .models import Contact, Label

class LabelSerializer(serializers.ModelSerializer):
    """
    연락처 라벨
    """
    class Meta:
        model = Label
        fields = ['id', 'name']

class ContactListSerializer(serializers.ModelSerializer):
    """
    연락처 목록
    """
    labels = LabelSerializer(many=True, read_only=True)

    class Meta:
        model = Contact
        fields = ['id', 'profile_url', 'name', 'email', 'phone', 'company', 'labels']

class ContactDetailSerializer(serializers.ModelSerializer):
    """
    연락처 상세 정보
    """
    labels = LabelSerializer(many=True, read_only=True)

    class Meta:
        model = Contact
        fields = [
            'id', 'profile_url', 'name', 'email', 'phone', 'company',
            'position', 'memo', 'labels', 'address', 'birthday', 'website'
        ]

class ContactCreateUpdateSerializer(serializers.ModelSerializer):
    """
    연락처 생성/수정
    """
    labels  = serializers.PrimaryKeyRelatedField(queryset=Label.objects.all(), many=True, required=False)
    
    """
    email validation: 이메일 형식 검사
    """
    def validate_email(self, value):
        if value and '@' not in value:
            raise serializers.ValidationError("이메일 형식이 올바르지 않습니다.")
        return value

    """
    phone validation: 전화번호 형식 검사
    """
    def validate_phone(self, value):
        # 전화번호는 숫자, +, -만 포함해야 하며, 최소 10자리 이상, 최대 15자리 이하
        if value and not all(c.isdigit() or c in ['+', '-'] for c in value):
            raise serializers.ValidationError("전화번호는 숫자, +, -만 포함할 수 있습니다.")
        if value and len(value) < 10:
            raise serializers.ValidationError("전화번호는 최소 10자리 이상이어야 합니다.")
        if value and len(value) > 15:
            raise serializers.ValidationError("전화번호는 최대 15자리 이하이어야 합니다.")
        return value
    
    """
    profile_url validation: URL 형식 검사
    """
    def validate_profile_url(self, value):
        if value and not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("프로필 URL은 http:// 또는 https://로 시작해야 합니다.")
        return value
    
    class Meta:
        model = Contact
        fields = [
            'profile_url', 'name', 'email', 'phone', 'company',
            'position', 'memo', 'labels', 'address', 'birthday', 'website'
        ]

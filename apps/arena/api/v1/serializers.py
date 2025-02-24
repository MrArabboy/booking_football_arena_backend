from rest_framework import serializers

from apps.account.models import User, UserRoleChoice
from apps.arena.models import FootballArena, FootballArenaImage


class FootballArenaCreateByArenaManagerSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)

    def create(self, validated_data):
        images = validated_data.pop("images")
        instance = super().create(validated_data)
        for image in images:
            FootballArenaImage.objects.create(arena=instance, image=image)
        return instance

    def update(self, instance, validated_data):
        images = validated_data.pop("images", None)
        instance = super().update(instance, validated_data)
        if images:
            instance.images.all().delete()
            for image in images:
                FootballArenaImage.objects.create(arena=instance, image=image)
        return instance

    class Meta:
        model = FootballArena
        fields = (
            "name",
            "address",
            "phone_number",
            "telegram_username",
            "description",
            "cover_image",
            "cost_per_hour",
            "latitude",
            "longitude",
            "images",
            "owner",
        )


class FootballArenaCreateByAdminSerializer(FootballArenaCreateByArenaManagerSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role=UserRoleChoice.ADMIN)
    )

    class Meta:
        model = FootballArena
        fields = FootballArenaCreateByArenaManagerSerializer.Meta.fields


class FootballArenaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FootballArena
        fields = (
            "id",
            "name",
            "address",
            "phone_number",
            "telegram_username",
            "cover_image",
            "cost_per_hour",
            "latitude",
            "longitude",
        )


class FootballArenaImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FootballArenaImage
        fields = ("id", "image")


class FootballArenaDetailSerializer(serializers.ModelSerializer):
    images = FootballArenaImageListSerializer(many=True)

    class Meta:
        model = FootballArena
        fields = (
            "id",
            "name",
            "address",
            "phone_number",
            "telegram_username",
            "description",
            "cover_image",
            "cost_per_hour",
            "latitude",
            "longitude",
            "images",
        )

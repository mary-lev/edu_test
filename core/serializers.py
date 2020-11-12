from rest_framework import serializers

from .models import (
            Student, Module, Stream,
            Lesson, Task, Feedback, Solution
            )


class ModuleSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='core:module')

    class Meta:
        model = Module
        fields = "__all__"


class StreamSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='core:stream')
    module = ModuleSerializer()

    class Meta:
        model = Stream
        fields = "__all__"


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='core:student')
    stream = StreamSerializer(many=True, read_only=False)

    class Meta:
        model = Student
        fields = "__all__"


class LessonSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='core:lesson')
    module = ModuleSerializer(read_only=False)

    class Meta:
        model = Lesson
        fields = "__all__"


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='core:task')
    lesson = LessonSerializer(read_only=False)

    class Meta:
        model = Task
        fields = "__all__"

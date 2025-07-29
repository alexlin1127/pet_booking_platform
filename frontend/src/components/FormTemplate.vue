<script setup>
defineProps({
    title: {
        type: String,
        required: true
    },
})

const emit = defineEmits(['submit'])

const onSubmit = () => {
    emit('submit')
}
</script>

<template>
    <div class="form-template-container">
        <!-- 表單標題 -->
        <h1 class="form-template-title">{{ title }}</h1>

        <!-- 表單內容插槽 -->
        <form @submit.prevent="onSubmit" class="form-template-content">
            <slot></slot>

            <!-- 按鈕區域 -->
            <div class="form-template-actions">
                <slot name="actions"></slot>
            </div>
        </form>
    </div>
</template>

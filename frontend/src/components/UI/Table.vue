<script setup></script>

<template>
        <table class="table">
        <thead>
            <tr class="table-header">
                <slot name="header"></slot>
            </tr>
        </thead>
        <tbody class="table-body">
            <slot name="body"></slot>
        </tbody>
    </table>
</template>



<style></style>
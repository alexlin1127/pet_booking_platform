<script setup>
import { bookings } from '../../../data/bookingfakedata'

const props = defineProps({
    watchItem: Object
});

function removeFromWatchList() {
    const idx = bookings.findIndex(b => b.id === props.watchItem.id)
    if (idx !== -1) {
        bookings[idx] = { ...bookings[idx], blacklist: false }
    }
}
</script>

<template>
    <td class="watchlist-card-cell">{{ watchItem.id }}</td>
    <td class="watchlist-card-cell">{{ watchItem.customer_name }}</td>
    <td class="watchlist-card-cell">{{ watchItem.phone }}</td>
    <td class="watchlist-card-cell">{{ watchItem.service_type }}</td>
    <td class="watchlist-card-cell">{{ watchItem.booking_date }}</td>
    <td class="watchlist-card-cell">{{ watchItem.note || '無' }}</td>
    <td class="watchlist-card-cell">
        <span class="watchlist-status-badge">觀察中</span>
        <button class="watchlist-remove-btn" @click="removeFromWatchList">移除觀察</button>
    </td>
</template>

<style scoped>
.watchlist-card-cell {
    padding: 12px;
    font-size: 14px;
}

.watchlist-status-badge {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 4px;
    background-color: #fef3c7;
    color: #92400e;
    font-size: 12px;
    margin-right: 8px;
}

.watchlist-remove-btn {
    padding: 4px 8px;
    border-radius: 4px;
    background-color: #fee2e2;
    color: #b91c1c;
    font-size: 12px;
    border: none;
    cursor: pointer;
    transition: background-color 0.2s;
}

.watchlist-remove-btn:hover {
    background-color: #fecaca;
}
</style>

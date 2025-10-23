import { defineStore } from "pinia";

export const useAppStore = defineStore('app', {
    state: () => ({
        baseUrlServer: '', // set server url
        fakeData: [
            {
                id: 1,
                title: 'Мефедрончик',
                price: 20,
                rating: 3.4
            },
            {
                id: 2,
                title: 'Гашиш',
                price: 25,
                rating: 3.9
            },
            {
                id: 3,
                title: 'Трава',
                price: 10,
                rating: 4.9
            },
            {
                id: 4,
                title: 'Амфетамин',
                price: 21,
                rating: 4.4
            },
            {
                id: 5,
                title: 'Спайс',
                price: 26,
                rating: 4.3
            },
            {
                id: 6,
                title: 'Грибочки',
                price: 13,
                rating: 3.9
            },
            {
                id: 7,
                title: 'Экстази',
                price: 15,
                rating: 4.9
            },
            {
                id: 8,
                title: 'Фентанил',
                price: 7,
                rating: 1.3
            },
            {
                id: 9,
                title: 'Героин',
                price: 22,
                rating: 4.2
            },
            {
                id: 10,
                title: 'Кокаин',
                price: 40,
                rating: 4.9
            }
        ]
    }),
    actions: {

    }
})
const { createApp } = Vue
createApp({
	delimiters: ['${', '}$'],
	mixins: [window.mix ? window.mix : {}],
	methods: {
		getCookie(name) {
			let cookieValue = null
			if (document.cookie && document.cookie !== '') {
				const cookies = document.cookie.split(';')
				for (let i = 0; i < cookies.length; i++) {
					const cookie = cookies[i].trim()
					// Does this cookie string begin with the name we want?
					if (cookie.substring(0, name.length + 1) === name + '=') {
						cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
						break
					}
				}
			}
			return cookieValue
		},
		postData(url, payload, headers = {}) {
		    console.log('POST запрос на URL:', url);
			return axios
				.post(url, payload, {
					headers: {
						'X-CSRFToken': this.getCookie('csrftoken'),
						'Content-Type': 'application/json',
						...(headers || {}),
					},
				})
				.then((response) => {
					return {
						data: response?.data,
						status: response.status,
					}
//					return response.data ? response.data : response.json?.()
				})
				.catch((error) => {
					console.warn(
						`Метод '${url}' вернул статус код ${error.response.status}`
					)
					throw new Error()
				})
		},
		getData(url, payload) {
			return axios
				.get(url, { params: payload })
				.then((response) => {
					return response.data ? response.data : response.json?.()
				})
				.catch(() => {
					console.warn('Метод ' + url + ' не реализован')
					throw new Error('no "get" method')
				})
		},
		search() {
			location.assign(`/catalog/?filter=${this.searchText}`)
		},
		getCategories() {
			this.getData('/api/categories/')
				.then((data) => (this.categories = data.results))
				.catch(() => {
					console.warn('Ошибка получения категорий')
					this.categories = []
				})
		},
		getBasket() {
			this.getData('/api/basket/')
				.then((data) => {
					const basket = {}
					data.forEach((item) => {
						basket[item.id] = {
							...item,
						}
					})
					this.basket = basket
				})
				.catch(() => {
					console.warn('Ошибка при получении корзины')
					this.basket = {}
				})
		},
		// getLastOrder() {
		// 	this.getData('/api/orders/active/')
		// 		.then(data => {
		// 			this.order = {
		// 				...this.order,
		// 				...data
		// 			}
		// 		})
		// 		.catch(() => {
		// 			console.warn('Ошибка при получении активного заказа')
		// 			this.order = {
		// 				...this.order,
		// 			}
		// 		})
		// },
		addToBasket(item, count = 1) {
			const { id } = item
			this.postData('/api/basket/', { id, count })
				.then(({ data }) => {
					this.basket = data
					alert('Товар добавлен в корзину. \nПродолжайте покупки \nили перейдите в корзину для оплаты.')
				})
				.catch(() => {
					console.warn('Ошибка при добавлении заказа в корзину')
					alert('Произошла ошибка при добавлении товара в корзину')
				})
		},
		removeFromBasket(id, count) {
			axios
				.delete('/api/basket/', {
					data: JSON.stringify({ id, count }),
					headers: {
						'X-CSRFToken': this.getCookie('csrftoken'),
						'Content-Type': 'application/json',
					},
				})
				.then(({ data }) => {
					this.basket = data
				})
				.catch(() => {
					console.warn('Ошибка при удалении заказа из корзины')
				})
		},
		signOut() {
			this.postData('/api/sign-out/').finally(() => {
				location.assign(`/`)
			})
		},
	},
	computed: {
		basketCount() {
			return (
				(this.basket &&
					Object.values(this.basket)?.reduce(
						(acc, { count, price }) => {
							acc.count += count
							acc.price += count * price
							return acc
						},
						{ count: 0, price: 0 }
					)) ?? { count: 0, price: 0 }
			)
		},
	},
	data() {
		return {
			// catalog page
			filters: {
				price: {
					minValue: 1,
					maxValue: 500000,
					currentFromValue: 7,
					currentToValue: 27,
				},
			},
			sortRules: [
				{ id: 'rating', title: 'Популярности' },
				{ id: 'price', title: 'Цене' },
				{ id: 'reviews', title: 'Отзывам' },
				{ id: 'date', title: 'Новизне' },
			],
			topTags: [],
			// reused data
			categories: [],
			// reused data
			catalogFromServer: [],
			orders: [],
			cart: [],
			paymentData: {},
			basket: {},
			// order: {
			// 	orderId: null,
			// 	createdAt: '',
			// 	products: [],
			// 	fullName: '',
			// 	phone: '',
			// 	email: '',
			// 	deliveryType: '',
			// 	city: '',
			// 	address: '',
			// 	paymentType: '',
			// 	totalCost: 0,
			// 	status: ''
			// },
			searchText: '',
		}
	},
	mounted() {
		this.getCategories()
		this.getBasket()
		// this.getLastOrder()
	},
}).mount('#site')

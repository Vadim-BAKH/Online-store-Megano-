var mix = {
  methods: {
    getBanners() {
      this.getData("/api/banners/")
        .then(data => {
          this.banners = (data || []).map(b => ({
            ...b,
            images: Array.isArray(b.images) ? b.images : []
          }));
        })
        .catch(() => {
          this.banners = [];
          console.warn('Ошибка при получении баннеров');
        });
    },
    getPopularProducts() {
      this.getData("/api/products/popular/")
        .then(data => {
          // data — массив, не меняем
          this.popularCards = (data || []).map(card => ({
            ...card,
            images: Array.isArray(card.images) ? card.images : []
          }));
        })
        .catch(error => {
          console.log('----', error);
          this.popularCards = [];
          console.warn('Ошибка при получении списка популярных товаров');
        });
    },
    getLimitedProducts() {
      this.getData("/api/products/limited/")
        .then(data => {
          // Берём data.results, т.к. приходит с пагинацией
          this.limitedCards = Array.isArray(data.results)
            ? data.results.map(card => ({
                ...card,
                images: Array.isArray(card.images) ? card.images : []
              }))
            : [];
        })
        .catch(() => {
          this.limitedCards = [];
          console.warn('Ошибка при получении списка лимитированных товаров');
        });
    }
  },
  mounted() {
    this.getBanners();
    this.getPopularProducts();
    this.getLimitedProducts();
  },
  data() {
    return {
      banners: [],
      popularCards: [],
      limitedCards: [],
    }
  }
}


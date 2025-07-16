var mix = {
  methods: {
    async getHistoryOrder() {
      try {
        const data = await this.getData("/api/history-order/");
        console.log(data);
        this.orders = data;
      } catch (error) {
        this.orders = [];
        console.warn('Ошибка при получении списка заказов', error);
      }
    }
  },
  async mounted() {
    await this.getHistoryOrder();
  },
  data() {
    return {
      orders: [],
    };
  }
}

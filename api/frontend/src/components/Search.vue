<template>
  <div class="search-container">
    <div class="search-box">
      <input 
        v-model="searchTerm" 
        placeholder="Digite nome ou CNPJ..."
        @keyup.enter="search"
        class="search-input"
      />
      <button @click="search" class="search-button">
        <span class="search-icon">🔍</span> Buscar
      </button>
    </div>

    <div v-if="loading" class="loading-message">Carregando...</div>
    
    <div v-if="error" class="error-message">{{ error }}</div>

    <div v-if="results.length > 0" class="results-container">
      <div v-for="item in results" :key="item.Registro_ANS" class="result-card">
        <h3 class="result-title">{{ item.Razao_Social }}</h3>
        <p class="result-detail"><strong>CNPJ:</strong> {{ item.CNPJ }}</p>
        <p class="result-detail"><strong>Registro ANS:</strong> {{ item.Registro_ANS }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchTerm: '',
      results: [],
      loading: false,
      error: ''
    }
  },
  methods: {
    async search() {
      if (!this.searchTerm.trim()) return;
      
      this.loading = true;
      this.error = '';
      this.results = [];
      
      try {
        const response = await fetch(
          `http://localhost:5000/search?q=${encodeURIComponent(this.searchTerm)}`
        );

        if (!response.ok) {
          throw new Error(`Erro: ${response.status}`);
        }

        const data = await response.json();
        this.results = data;
        
      } catch (err) {
        console.error("Erro completo:", err);
        this.error = 'Erro ao buscar dados. Tente novamente.';
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.search-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.search-box {
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
}

.search-input {
  flex: 1;
  padding: 12px 15px;
  border: 2px solid #42b983;
  border-radius: 6px;
  font-size: 16px;
  transition: all 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #2c3e50;
  box-shadow: 0 0 0 3px rgba(66, 185, 131, 0.2);
}

.search-button {
  padding: 12px 25px;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-button:hover {
  background: #369f6e;
  transform: translateY(-2px);
}

.search-icon {
  font-size: 18px;
}

.loading-message {
  text-align: center;
  padding: 20px;
  color: #42b983;
  font-style: italic;
}

.error-message {
  text-align: center;
  padding: 20px;
  color: #e74c3c;
  font-weight: bold;
}

.results-container {
  display: grid;
  gap: 15px;
}

.result-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

.result-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.result-title {
  color: #2c3e50;
  margin-top: 0;
  margin-bottom: 10px;
}

.result-detail {
  color: #34495e;
  margin: 5px 0;
}

.result-detail strong {
  color: #42b983;
}
</style>
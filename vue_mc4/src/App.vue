<template>
  <div id="wrapper">
    <nav class="navbar-brand">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>Django Testing</strong></router-link>

        <a aria-label="menu" aria-expanded="false" data-target="navbar-menu" class="navbar-burger">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div class="navbar-menu" id="navbar-menu">
        <div class="navbar-end">
          <div class="navbar-item">
            <div class="buttons">
            </div>
          </div>
        </div>
      </div>
    </nav>

    <section class="section">
      <div class="container">
        <div class="columns is-centered">
          <div class="column is-4-desktop is-6-tablet">
            <h1 class="title has-text-centered">
              {{ isRegister ? 'Registro' : 'Inicio de sesion' }}
            </h1>

            <form @submit.prevent="sendData" class="box">
              <div v-if="isRegister" class="field">
                <label class="label" for="companyName">Nombre de la empresa</label>
                <div class="control has-icons-left">
                  <input
                    v-model="companyName"
                    class="input"
                    type="text"
                    id="companyName"
                    name="companyName"
                    placeholder="e.g. Empresa S.A."
                    required
                  />
                  <span class="icon is-small is-left">
                    <i class="fas fa-user"></i>
                  </span>
                </div>
              </div>

                <div v-else class="field">
                  <label class="label" for="Usuario">Usuario</label>
                  <div class="control has-icons-left">
                    <input
                      v-model="Usuario"
                      class="input"
                      type="text"
                      id="usuario"
                      name="usuario"
                      placeholder="e.g. ejemplo123"
                      required
                    />
                    <span class="icon is-small is-left">
                      <i class="fas fa-envelope"></i>
                    </span>
                  </div>
                </div>

              <div v-if="isRegister" class="field">
                <label class="label" for="numeroCuenta">Numero de Cuenta</label>
                <div class="control has-icons-left">
                  <input
                    v-model="numeroCuenta"
                    class="input"
                    type="text"
                    id="numeroCuenta"
                    name="numeroCuenta"
                    placeholder="e.g. 000"
                    required
                  />
                  <span class="icon is-small is-left">
                    <i class="fas fa-envelope"></i>
                  </span>
                </div>
              </div>

              <div v-else class="field">
                <label class="label" for="password">Contraseña</label>
                <div class="control has-icons-left">
                  <input
                    v-model="password"
                    class="input"
                    type="password"
                    id="password"
                    name="password"
                    placeholder="********"
                    required
                  />
                  <span class="icon is-small is-left">
                    <i class="fas fa-lock"></i>
                  </span>
                </div>
              </div>

              <div class="field" v-if="!isRegister">
                <label class="checkbox">
                  <input v-model="remember" type="checkbox" />
                  Remember me
                </label>
              </div>

              <div class="field">
                <button type="submit" class="button is-primary is-fullwidth">
                  {{ isRegister ? 'Registro' : 'Ingresar' }}
                </button>
              </div>

              <div class="field has-text-centered">
                <a @click.prevent="isRegister = !isRegister">
                  {{ isRegister ? 'Ya tienes una cuenta? Inicia sesión' : "No tienes una cuenta? Registrate" }}
                </a>
              </div>

              <p v-if="error" class="has-text-danger has-text-centered">
                {{ error }}
              </p>
              <p v-if="success" class="has-text-success has-text-centered">
                {{ success }}
              </p>
            </form>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>


export default {
  name: 'App',
  data() {
    return {
      email: '',
      password: '',
      remember: false,
      error: '',
      success: '',
      isRegister: false
    };
  },
  methods: {
    async sendData() {
      this.error = '';
      this.success = '';

      try {
        const formData = new FormData();
        if (this.isRegister) {
          formData.append('companyName', this.companyName);
          formData.append('numeroCuenta', this.numeroCuenta);
          formData.append('register_submit', true);
        } else {
          formData.append('usuario', this.usuario);
          formData.append('password', this.password);
          formData.append('remember', this.remember);
          formData.append('login_submit', true);
        }

        const response = await this.$http.post('/api/data/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });

        if (response.data && response.data.success) {
          this.success = response.data.message || 'Inicio de sesion exitoso';
        } else {
          this.error = response.data.message || 'Error de inicio de sesion. Por favor, intente de nuevo.';
        }
      } catch (err) {
        console.error('Error sending form data:', err);
        this.error = 'Login failed. Please try again.';
      }
    }
  }
};
</script>

<style lang="scss">
@import '../node_modules/bulma'
</style>

<template>
  <div id="talen_selector"> 
    <multiselect v-model="value" 
      placeholder="Kies taal" 
      label="name" 
      track-by="code" 
      :options="options" :multiple="true" 
      :taggable="false" @input="updateValue">
    </multiselect>
    <textarea name="talen" v-model="json_value" id="talen_json_value"></textarea>
    <pre class="language-json" id="talen_value_preview"><code>{{ value  }}</code></pre>
</div>
</template>

<script>
  import Multiselect from 'vue-multiselect'

  // example: initial languages to show on loading metadata item
  var default_value = [{ name: 'Nederlands', code: 'nl' }, { name: 'Frans', code: 'fr' } ]  

  var pid = document.getElementById("pid").innerText;
  console.log("vue component received pid=", pid );

  export default {
    name: 'TalenSelector',
    components: {
      Multiselect 
    },
    data () {
      return {
        value: default_value,
        json_value: JSON.stringify(default_value),
        options: [
          { name: 'Nederlands', code: 'nl' },
          { name: 'Frans', code: 'fr' },
          { name: 'Duits', code: 'de' },
          { name: 'Italiaans', code: 'it' },
          { name: 'Engels', code: 'en' },
          { name: 'Spaans', code: 'es' },
          { name: 'Afar', code: 'aa' },
          { name: 'Abchazisch', code: 'ab' },
          { name: 'Afrikaans', code: 'af' },
          { name: 'Amhaars', code: 'am' },
          { name: 'Arabisch', code: 'ar' },
          { name: 'Assamees', code: 'as' },
          { name: 'Aymara', code: 'ay' },
          { name: 'Azerbeidzjaans', code: 'az' },
          { name: 'Basjkir', code: 'ba' },
          { name: 'Wit-Russisch', code: 'be' },
          { name: 'Bislama', code: 'bi' },
          { name: 'Bengaals', code: 'bn' },
          { name: 'Tibetaans', code: 'bo' },
          { name: 'Bretons', code: 'br' },
          { name: 'Catalaans', code: 'ca' },
          { name: 'Tsjechisch', code: 'cs' },
          { name: 'Welch', code: 'cy' },
          { name: 'Deens', code: 'da' },
          { name: 'Bhutani', code: 'dz' },
          { name: 'Grieks', code: 'el' },
          { name: 'Esperanto', code: 'eo' },
          { name: 'Ests', code: 'et' },
          { name: 'Baskisch', code: 'eu' },
          { name: 'Perzisch', code: 'fa' },
          { name: 'Fins', code: 'fi' },
          { name: 'Fiji', code: 'fj' },
          { name: 'Iers', code: 'ga' },
          { name: 'Schots Gaelic', code: 'gd' },
          { name: 'Galicisch', code: 'gl' },
          { name: 'Guarani', code: 'gn' },
          { name: 'Gujarati', code: 'gu' },
          { name: 'Hausa', code: 'ha' },
          { name: 'Hebreeuws', code: 'he' },
          { name: 'Hindi', code: 'hi' },
          { name: 'Hongaars', code: 'hu' },
          { name: 'Kroatisch', code: 'hr' },
          { name: 'Hongaars', code: 'hu' },
          { name: 'Armeens', code: 'hy' },
          { name: 'Interlingua', code: 'ia' },
          { name: 'Indonesisch', code: 'id' },
          { name: 'Interlingue', code: 'ie' },
          { name: 'Inupiak', code: 'ik' },
          { name: 'IJslands', code: 'is' },
          { name: 'Inuktitut (Eskimo)', code: 'iu' },
          { name: 'Japans', code: 'ja' },
          { name: 'Georgisch', code: 'ka' },
          { name: 'Kazachs', code: 'kk' },
          { name: 'Groenlands', code: 'kl' },
          { name: 'Cambodjaans', code: 'km' },
          { name: 'Kannada', code: 'kn' },
          { name: 'Koreaans', code: 'ko' },
          { name: 'Kasjmir', code: 'ks' },
          { name: 'Koerdisch', code: 'ku' },
          { name: 'Kirgizisch', code: 'ky' },
          { name: 'latijns', code: 'la' },
          { name: 'Lingala', code: 'ln' },
          { name: 'Laotiaans', code: 'lo' },
          { name: 'Litouws', code: 'lt' },
          { name: 'Lets, Lets', code: 'lv' },
          { name: 'Malagasi', code: 'mg' },
          { name: 'Macedonisch', code: 'mk' },
          { name: 'Malayalam', code: 'ml' },
          { name: 'Mongools', code: 'mn' },
          { name: 'Marathi', code: 'mr' },
          { name: 'Maleis', code: 'ms' },
          { name: 'Maltees', code: 'mt' },
          { name: 'Birmaans', code: 'my' },
          { name: 'Nauru', code: 'na' },
          { name: 'Nepalees', code: 'ne' },
          { name: 'Noors', code: 'no' },
          { name: 'Occitaans', code: 'oc' },
          { name: '(Afan) Oromo', code: 'om' },
          { name: 'Oriya', code: 'or' },
          { name: 'Punjabi', code: 'pa' },
          { name: 'Pools', code: 'pl' },
          { name: 'Pashto, Pushto', code: 'ps' },
          { name: 'Portugees', code: 'pt' },
          { name: 'Quechua', code: 'qu' },
          { name: 'Reto-Romaans', code: 'rm' },
          { name: 'Kirundi', code: 'rn' },
          { name: 'Roemeens', code: 'ro' },
          { name: 'Russisch', code: 'ru' },
          { name: 'Kinyarwanda', code: 'rw' },
          { name: 'Sanskriet', code: 'sa' },
          { name: 'Sindhi', code: 'sd' },
          { name: 'Sangro', code: 'sg' },
          { name: 'Servo-Kroatisch', code: 'sh' },
          { name: 'Singalees', code: 'si' },
          { name: 'Slowaaks', code: 'sk' },
          { name: 'Sloveens', code: 'sl' },
          { name: 'Samoaans', code: 'sm' },
          { name: 'Shona', code: 'sn' },
          { name: 'Somalisch', code: 'so' },
          { name: 'Albanees', code: 'sq' },
          { name: 'Servisch', code: 'sr' },
          { name: 'Siswati', code: 'ss' },
          { name: 'Sesotho', code: 'st' },
          { name: 'Soedanees', code: 'su' },
          { name: 'Zweeds', code: 'sv' },
          { name: 'Swahili', code: 'sw' },
          { name: 'Tamil', code: 'ta' },
          { name: 'Telugu', code: 'te' },
          { name: 'Tadzjieks', code: 'tg' },
          { name: 'Thais', code: 'th' },
          { name: 'Tigrinya', code: 'ti' },
          { name: 'Turkmeens', code: 'tk' },
          { name: 'Tagalog', code: 'tl' },
          { name: 'Setswana', code: 'tn' },
          { name: 'Tonga', code: 'to' },
          { name: 'Turks', code: 'tr' },
          { name: 'Tsonga', code: 'ts' },
          { name: 'Tataars', code: 'tt' },
          { name: 'twee keer', code: 'tw' },
          { name: 'Oeigoers', code: 'ug' },
          { name: 'Oekraïens', code: 'uk' },
          { name: 'Urdu', code: 'ur' },
          { name: 'Oezbeeks', code: 'uz' },
          { name: 'Vietnamees', code: 'vi' },
          { name: 'Volapuk', code: 'vo' },
          { name: 'Wolof', code: 'wo' },
          { name: 'Xhosa', code: 'xh' },
          { name: 'Jiddisch', code: 'yi' },
          { name: 'Yoruba', code: 'yo' },
          { name: 'Zhuang', code: 'za' },
          { name: 'Chinees', code: 'zh' },
          { name: 'Zulu', code: 'zu' },
        ]
      }
    },
    methods: {
      updateValue(value){
        this.json_value = JSON.stringify(value)
      }
    }
  }
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style>
  #talen_selector{
    min-width: 30em;
  }

  #talen_json_value{
    display: none;
    width: 80%;
    height: 100px;
    margin-top: 20px;
    margin-bottom: 20px;
  }

  #talen_value_preview{
    display: none;
    margin-bottom: 20px;
  }

</style>

<template>
  <div>
    <div class="q-pa-md">
      <q-table
        title="Backlinks"
        :rows="rows"
        :columns="columns"
        row-key="name"
        :loading="loading"
      >
        <template v-slot:top>
          <q-btn
            icon="link"
            unelevated
            rounded
            color="positive"
            text-color="white"
            label="Toevoegen"
            class="q-mr-sm"
            @click="addSiteModal"
          />
          <q-btn
            icon="find_in_page"
            unelevated
            rounded
            color="primary"
            text-color="white"
            label="Scan alle links"
            @click="scanLinks(selected)"
          />
        </template>
        <template v-slot:body-cell-actions="props">
          <q-td>
            <q-btn-dropdown flat dropdown-icon="more_horiz">
              <q-list bordered>
                <q-item clickable v-ripple>
                  <q-item-section avatar>
                    <q-icon color="primary" name="find_in_page" size="sm"/>
                  </q-item-section>
                  <q-item-section>Scan</q-item-section>
                </q-item>
                <q-item clickable v-ripple @click="deleteLink(props.row.id, props.pageIndex)">
                  <q-item-section avatar>
                    <q-icon color="negative" name="delete_forever" size="sm"/>
                  </q-item-section>
                  <q-item-section>Verwijder</q-item-section>
                </q-item>
              </q-list>

            </q-btn-dropdown>
          </q-td>
        </template>
        <template v-slot:body-cell-status="props">
          <q-td :props="props">
            <div>
              <q-icon
                size="sm"
                name="verified"
                square
                color="positive"
                v-if="props.value === true"
              />
              <q-icon size="sm" name="warning" square color="negative" v-else />
            </div>
          </q-td>
        </template>
      </q-table>
    </div>

    <q-dialog v-model="newLinkModal">
      <q-card style="width: 700px; max-width: 80vw">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Link toevoegen</div>
          <q-space />
          <q-btn icon="close" size="sm" flat round dense v-close-popup />
        </q-card-section>

        <q-card-section>
          <q-form>
            <q-input
              oulined
              type="url"
              v-model="newLink.link"
              label="Link die je wilt controleren"
            />
            <q-input
              oulined
              type="url"
              v-model="newLink.site"
              label="Website waar de link is geplaatst"
            />
          </q-form>
        </q-card-section>
        <q-card-actions class="flex justify-end">
          <q-btn
            type="submit"
            icon="add"
            label="Toevoegen"
            color="primary"
            unelevated
            class="q-ma-sm"
            rounded
            @click="addNewLink"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import { data } from "autoprefixer";
import { ref } from "vue";
const columns = [
  {
    name: "actions",
    label: "Akties",
    align: "left",
    sortable: false,
  },
  {
    name: "desc",
    required: true,
    label: "Link",
    align: "left",
    field: (row) => row.link,
    format: (val) => `${val}`,
    sortable: true,
  },
  {
    name: "site",
    required: true,
    label: "Website",
    align: "left",
    field: "site",
    sortable: true,
  },
  {
    name: "da",
    required: true,
    label: "DA",
    align: "left",
    field: "da",
    sortable: true,
  },
  {
    name: "pa",
    required: true,
    label: "PA",
    align: "left",
    field: "pa",
    sortable: true,
  },
  {
    name: "status",
    required: true,
    label: "Status",
    align: "left",
    field: "status",
    sortable: true,
  },
  {
    name: "last_check",
    required: true,
    label: "Laatste check",
    align: "left",
    field: "last_check",
    sortable: true,
  },
];

export default {
  setup() {
    const selected = ref([]);
  },
  data() {
    return {
      selected: [],
      rows: [],
      columns,
      loading: false,
      refreshButton: false,
      newLinkModal: false,
      newLink: { site: "", link: "" },
    };
  },
  methods: {
    addSiteModal() {
      this.newLinkModal = true;
    },
    addNewLink() {
      // send to API if succesfull:
      this.$api
        .post("backlinks", {
          link: this.newLink.link,
          site: this.newLink.site,
          status: "null",
          pa: "?",
          da: "?",
          last_check: "?",
        })
        .then((response) => {
          this.rows.push(response.data);
          this.newLink.site = ""
          this.newLink.link = ""
          this.newLinkModal = true;
        });

    },
    async scanLinks(links) {
      this.$q.loading.show({
        message: "Sites worden gescand...",
      });
      await this.$api
        .get("backlinks/scan")
        .then((response) => {
          this.$q.loading.hide();
          this.$q.notify({
            message: "Scan geslaagd",
            type: "positive",
          });
        });
    },
    deleteLink(id, i){
      this.$api.delete(`backlinks/${id}`).then((response)=>{
        this.rows.splice(i, 1);
        this.$q.notify({
          type:'positive',
          message:response.data
        })
      })
    }
  },
  watch: {
    selected(v) {
      if (v.length > 0) {
        this.refreshButton = true;
      } else {
        this.refreshButton = false;
      }
    },
  },
  mounted() {
    this.$api.get("backlinks").then((response) => {
      this.rows = response.data;
    });
  },
};
</script>

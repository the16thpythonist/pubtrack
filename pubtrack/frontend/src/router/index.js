import Vue from "vue";

// VIEW COMPONENTS
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import NotFound from "../views/NotFound";
import KITOpenCoverage from "../views/KITOpenCoverage";
import AuthorList from "../views/AuthorList";
import AuthorDetail from "../views/AuthorDetail";
import PublicationList from "../views/PublicationList";
import PublicationDetail from "../views/PublicationDetail";

Vue.use(VueRouter);

// /analytics/publications/kitopen-coverage/

const routes = [
  {
    path: "/",
    name: "home",
    component: Home
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue")
  },
  {
    path: "/analytics/publications/kitopen-coverage",
    name: "kitopen-coverage",
    component: KITOpenCoverage
  },
  {
    path: "/authors",
    name: "authors-list",
    component: AuthorList
  },
  {
    path: "/authors/:slug",
    name: "author-detail",
    component: AuthorDetail,
    props: true
  },
  {
    path: "/publications",
    name: "publications-list",
    component: PublicationList,
  },
  {
    path: "/publications/:uuid",
    name: "publication-detail",
    component: PublicationDetail,
    props: true
  },
  {
    path: "*",
    name: "page-not-found",
    component: NotFound
  }
];

const router = new VueRouter({
  mode: "history",
  // base: process.env.BASE_URL,
  routes
});

export default router;

Rails.application.routes.draw do
  resources :recipes
  resources :modifications
  resources :votes
  resources :subscribers

  get 'search', to: 'search#search'
  get 'welcome/index'
  root 'welcome#index'
end

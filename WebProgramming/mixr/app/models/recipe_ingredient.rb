class RecipeIngredient
  include Mongoid::Document
  field :quantity, type: String
  
  has_many :modifications, as: :original
  belongs_to :ingredient
  belongs_to :recipe
end

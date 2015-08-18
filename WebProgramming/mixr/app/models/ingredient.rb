class Ingredient
  include Mongoid::Document
  field :name, type: String

  has_many :recipe_ingredients

  validates :name, presence: true, length: { minimum: 2, maximum: 255 },
            uniqueness: { case_sensitive: false }

  before_save :convert_to_lower_case
  

  protected
    def convert_to_lower_case
      self.name = name.downcase 
    end
end

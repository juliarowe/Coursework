class Step
  include Mongoid::Document
  field :instruction, type: String

  has_many :modifications, as: :original
  belongs_to :recipe

  validates :instruction, presence: true, length: { minimum: 2, maximum: 255 }
end

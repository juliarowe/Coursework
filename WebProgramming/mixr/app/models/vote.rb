class Vote
  include Mongoid::Document
  field :value, type: Float

  belongs_to :rateable, polymorphic: true

  validates :value, presence: true, numericality: { greater_than_or_equal_to: 0,
                                                    less_than_or_equal_to: 5 }
end

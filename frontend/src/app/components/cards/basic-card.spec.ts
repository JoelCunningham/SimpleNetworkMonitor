import { BasicCard } from '#components/cards/basic-card';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('BasicCard', () => {
  let component: BasicCard;
  let fixture: ComponentFixture<BasicCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BasicCard],
    }).compileComponents();

    fixture = TestBed.createComponent(BasicCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
